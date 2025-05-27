import io
import json
import random
import string
from collections import defaultdict
from datetime import datetime, timedelta

import stripe
from dateutil import parser
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.forms.utils import ErrorDict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.timezone import localdate
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from DjangoAir import settings

from .forms import LoginForm, RegisterForm
from .models import (AirlineUser, Baggage, BoardingPass, Comfort, Flight, Meal,
                     Ticket, TicketStatusChoices)

stripe.api_key = settings.STRIPE_SECRET_KEY

# Generates a booking reference like 'A1B2C3D4E5'
def generate_booking_reference():
    """
    Generates a random 10-character booking reference consisting of
    uppercase letters and digits.

    Returns:
    - str: A 10-character alphanumeric booking reference.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Formats Django form or serializer errors into a plain dictionary
def format_errors(errors: ErrorDict) -> dict:
    """
    Converts a Django ErrorDict into a plain dictionary with lists of string messages.

    Parameters:
        errors (ErrorDict): A Django ErrorDict object containing field-specific error messages.

    Returns:
        dict: A dictionary where each key is a field name and the value is a list of error messages as strings.
    """
    formatted = {}
    for field, messages in errors.items():
        formatted[field] = [str(msg) for msg in messages]
    return formatted

# Generates a unique username by appending a number if needed
def generate_unique_username(base_username):
    """
    Generates a unique username based on the given base username.
    If the base username is already taken, appends a number and increments it until available.

    Parameters:
        base_username (str): The initial username to base the unique name on.

    Returns:
        str: A unique username that does not exist in the user model.
    """
    User = get_user_model()
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username

# Formats seat data into a readable string like "12A (Economy), 14B (Business)"
def formatted_seats(seats_data):
    """
    Formats a list of seat dictionaries into a readable string with seat ID and class.

    Parameters:
        seats_data (list): A list of dictionaries where each dictionary has:
            - 'id' (str or int): The seat identifier.
            - 'class' (str): The class of the seat (e.g., 'economy', 'business').

    Returns:
        str: A comma-separated string of formatted seat info.
              Example: "12A (Economy), 14B (Business)"
    """
    seats = [f"{seat['id']} ({seat['class'].capitalize()})" for seat in seats_data]
    return ', '.join(seats)

# Formats ISO flight time string into "DD.MM.YYYY HH:MM" format
def formatted_flight_time(flight_time):
    """
    Parses an ISO 8601 datetime string and formats it as "DD.MM.YYYY HH:MM".

    Parameters:
        flight_time (str): An ISO-formatted datetime string (e.g., "2025-05-27T14:30:00Z").

    Returns:
        str: A string representing the date and time in the format "DD.MM.YYYY HH:MM".
    """
    date_obj = parser.isoparse(flight_time)
    formatted_date = date_obj.strftime('%d.%m.%Y')
    formatted_time = date_obj.strftime('%H:%M')
    return f'{formatted_date} {formatted_time}'

# Handles Stripe webhook event when a payment is successfully completed
@csrf_exempt
def succeed_payment(request):
    """
    Processes the Stripe 'checkout.session.completed' webhook event.

    This function verifies the Stripe webhook signature, parses the event,
    and upon a successful payment:
    - Extracts metadata including seats and optional services (meals, baggage, comfort).
    - Creates Ticket objects for each seat with related services.
    - Assigns a gate and generates a booking reference.
    - Sends a confirmation email with ticket details to the user.

    Parameters:
        request (HttpRequest): The incoming HTTP request from Stripe's webhook.

    Returns:
        HttpResponse:
            - 200 OK on successful processing.
            - 400 Bad Request with appropriate error message if verification or data parsing fails.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if sig_header is None:
        print("⚠️  Missing Stripe signature header.")
        return HttpResponse("Missing signature", status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(f"⚠️  Invalid payload: {e}")
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"⚠️  Invalid signature: {e}")
        return HttpResponse("Invalid signature", status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        print(metadata)

        if 'seats' in metadata:
            try:
                seats = json.loads(metadata.get('seats', '[]'))
                services = json.loads(metadata.get('services', '{}'))
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON Decode Error: {e}")
                return HttpResponse("Invalid JSON in seats", status=400)

            meal_ids = [meal["id"] for meal in services.get("meals", [])]
            baggage_ids = [baggage["id"] for baggage in services.get("baggage", [])]
            comfort_ids = [comfort["id"] for comfort in services.get("comfort", [])]

            meal_objs = Meal.objects.filter(id__in=meal_ids)
            baggage_objs = Baggage.objects.filter(id__in=baggage_ids)
            comfort_objs = Comfort.objects.filter(id__in=comfort_ids)

            if comfort_objs.filter(id=1).exists():
                gate = 1
            else:
                gate = random.randint(2, 6)

            for seat in seats:
                ticket = Ticket.objects.create(
                    seat_number=seat['id'],
                    price=seat['price'],
                    flight_id=metadata['flight_id'],
                    passenger_id=metadata['user_id'],
                    seat_class=seat['class'],
                    booking_reference=generate_booking_reference(),
                    gate=gate,
                )

                ticket.meals.set(meal_objs)
                ticket.baggage.set(baggage_objs)
                ticket.comforts.set(comfort_objs)

                user = AirlineUser.objects.get(id=metadata['user_id'])
                user_email = user.email
                boarding_time = ticket.flight.departure_time - timedelta(minutes=30)

                subject = "Ваш квиток"
                context = {
                    "user": user,
                    "ticket": ticket,
                    "formatted_data": {
                        "date": ticket.flight.departure_time.strftime("%d.%m.%Y"),
                        "departure_time": ticket.flight.departure_time.strftime("%H:%M"),
                        "arrival_time": ticket.flight.arrival_time.strftime("%H:%M"),
                        "boarding_time": boarding_time.strftime("%H:%M"),
                    }
                }
                message_html = render_to_string("ticket_email.html", context)

                send_mail(
                    subject=subject,
                    message="Ваш email-клієнт не підтримує HTML.",  # Текстова версія (обов'язкова)
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email],  # має бути список
                    html_message=message_html,  # HTML-версія
                )
        else:
            print("⚠️ No seats found in metadata.")
            return HttpResponse("No seats in metadata", status=400)

    return HttpResponse(status=200)

# Function to retrieve the current user`s information
def current_user(request):
    """
    Checks if the user is authenticated and returns user information.

    Parameters:
    - request: The HTTP request

    Returns:
    - JsonResponse with the user`s information if authenticated.
    - JsonResponse with 'isAuthenticated': False if the user is not authenticated.
    """
    if request.user.is_authenticated:
        return JsonResponse({
            'isAuthenticated': True,
            'user': {
                'id': request.user.id,
                'name': f'{request.user.first_name} {request.user.last_name}',
                'email': request.user.email,
                'role': request.user.role
            }
        })
    else:
        return JsonResponse({
            'isAuthenticated': False, 'user': None
        })

# Home page with the list of flights
def index(request):
    """
    Renders the home page with Vue.js container

    Parameters:
    - GET request: The HTTP request

    Returns:
    - render: Renders the 'home.html' template with flight data and cities
    """
    flights = Flight.objects.all().order_by('destination', 'departure_time')
    flight_data = defaultdict(list)
    cities = set()

    for flight in flights:
        route = f"{flight.origin} → {flight.destination}"
        cities.add(route)

        seats_taken = Ticket.objects.filter(flight=flight).count()

        seats_total = 60
        seats_available = seats_total - seats_taken  # виправлено логіку (було навпаки)

        duration_td = flight.arrival_time - flight.departure_time
        hours, remainder = divmod(duration_td.seconds, 3600)
        minutes = remainder // 60
        duration_str = f'{hours}h {minutes}m'

        seats_taken = list(Ticket.objects.filter(flight_id=flight.id, status=TicketStatusChoices.UPCOMING).order_by('seat_number').values_list('seat_number', flat=True))

        flight_data[route].append({
            'date': flight.departure_time.isoformat(),
            'flight_id': flight.id,
            'time': flight.departure_time.strftime('%d.%m.%Y at %H:%M'),
            'airline': '',
            'aircraft': '',
            'gate': '',
            'terminal': '',
            'duration': duration_str,
            'price': float(flight.base_price),
            'seats_total': seats_total,
            'seats_available': seats_available,
            'taken': seats_taken,
        })

    return render(request, 'home.html', {
        'flight_dates': dict(flight_data),
        'unique_cities': sorted(cities),
    })

# Returns a list of tickets for the currently authenticated user in JSON format
def get_tickets(request):
    """
    Retrieves all tickets belonging to the currently authenticated user and
    returns them as a JSON response with flight and service details.

    For each ticket, the response includes:
    - Basic ticket info (ID, status, booking reference, gate, seat, price)
    - Flight info (origin, destination, times, duration, flight number)
    - Passenger info (name and formatted ID)
    - Boarding time (30 minutes before departure)
    - Additional services (meals, baggage, comforts) with relevant details

    Parameters:
        request (HttpRequest): The HTTP request containing the user session.

    Returns:
        JsonResponse: A list of ticket data in JSON format.
    """
    user_id = request.user.id
    tickets = Ticket.objects.filter(passenger__id=user_id).select_related('flight')

    data = []
    for ticket in tickets:
        flight = ticket.flight

        data.append({
            "id": ticket.id,
            "destination": flight.destination,
            "departureCity": flight.origin,  # можна розширити Flight для цього
            "departureCode": flight.origin_code,  # або отримати з Airport моделі
            "arrivalCode": flight.destination_code,
            "date": flight.departure_time.date().isoformat(),
            "departureTime": flight.departure_time.strftime("%H:%M"),
            "arrivalTime": flight.arrival_time.strftime("%H:%M"),
            "duration": str(flight.arrival_time - flight.departure_time),
            "flightNumber": flight.flight_number,
            "status": ticket.status,
            "passengerName": f"{ticket.passenger.first_name} {ticket.passenger.last_name}",
            "passengerId": f"P{ticket.passenger.id:08d}",  # умовний приклад
            "bookingReference": f"BR{ticket.id:06d}",  # умовний приклад
            "gate": ticket.gate,
            "boardingTime": (flight.departure_time - timedelta(minutes=30)).strftime("%H:%M"),
            "seats": [
                {
                    "id": ticket.seat_number,
                    "class": ticket.seat_class,
                    "price": float(ticket.price),
                }
            ],
            "totalAmount": float(ticket.price),
            "additional_services": {
                "meals": [
                    {
                        "name": meal.name,
                        "price": meal.price,
                        "dietaryOptions": [opt.name for opt in meal.dietary_options.all()],
                        "image": meal.image_url,
                    }
                    for meal in ticket.meals.all()
                ],
                "baggage": [
                    {
                        "name": bag.name,
                        "weight": bag.weight,
                        "price": bag.price,
                    }
                    for bag in ticket.baggage.all()
                ],
                "comforts": [
                    {
                        "name": comfort.name,
                        "description": comfort.description,
                        "price": comfort.price,
                    }
                    for comfort in ticket.comforts.all()
                ],
            }
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def cancel_ticket(request):
    """
    Cancels a ticket by setting its status to CANCELED.

    Expects a POST request with JSON body containing:
        {
            "ticket_id": <int>
        }

    Returns:
        - 200 OK with {"status": "success"} if the ticket was found and cancelled.
        - 404 if the ticket does not exist.
        - 400 for invalid JSON or missing ticket_id.
        - 405 if the method is not POST.
    """
    if request.method != 'POST':
        return JsonResponse(
            {'success': False, 'error': 'Invalid request method.'}, status=405
        )

    try:
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')

        if not ticket_id:
            return JsonResponse({'success': False, 'error': 'Missing ticket_id.'}, status=400)

        ticket = Ticket.objects.get(id=ticket_id)
        ticket.status = TicketStatusChoices.CANCELED
        ticket.save()

        return JsonResponse({'status': 'success'})

    except Ticket.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Ticket not found.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)


def additional_services(request):
    meals = Meal.objects.all()
    meals_data = []

    for meal in meals:
        meals_data.append({
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "price": meal.price,
            "image": meal.image_url,
            "dietary": [option.name for option in meal.dietary_options.all()],
            "price_id": meal.stripe_price_id,
        })

    baggage_options = Baggage.objects.all()
    baggage_data = []
    for baggage in baggage_options:
        baggage_data.append({
            "id": baggage.id,
            "name": baggage.name,
            "description": baggage.description,
            "price": baggage.price,
            "weight": baggage.weight,
            "price_id": baggage.stripe_price_id,
        })

    comfort_options = Comfort.objects.all()
    comfort_data = []
    for comfort in comfort_options:
        comfort_data.append({
            "id": comfort.id,
            "name": comfort.name,
            "description": comfort.description,
            "price": comfort.price,
            "price_id": comfort.stripe_price_id,
        })

    services_data = {
        "meals": meals_data,
        "baggage": baggage_data,
        "comfort": comfort_data,
    }

    return JsonResponse(services_data, safe=False)

def bookings(request):
    if request.user.is_authenticated:
        return render(request, 'bookings.html')


# Login view to handle user login
@csrf_protect
def login(request):
    """
    Handles the login functionality. It used custom authenticate backend (email and password) for authenticate.

    Parameters:
    - POST request: The HTTP request

    Returns:
    - JsonResponse with boolean success or failure, and with error message if needed.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                auth_login(request, user)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'name': f'{user.first_name} {user.last_name}',
                        'email': user.email,
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': {'general': 'Невірний email або пароль'}
                })
        else:
            # Сконвертувати form.errors до простого словника
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})

    return JsonResponse({'success': False, 'errors': {'general': 'Login failed. Invalid method.'}})


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']

            # Перевіряємо унікальність email
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'email': 'Користувач з таким email вже існує.'
                    }
                })

            # Створюємо базове ім’я користувача
            base_username = email.split('@')[0]

            # Створюємо користувача
            user = form.save(commit=False)
            user.set_password(password)
            if User.objects.filter(username=base_username).exists():
                username = generate_unique_username(base_username)
                user.username = username
            else:
                user.username = base_username
            user.email = email
            user.save()

            # Аутентифікація
            user = authenticate(request, email=email, password=password)
            if user:
                user.backend = 'air.backends.EmailBackend'
                auth_login(request, user)

                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'name': f'{user.first_name} {user.last_name}',
                    }
                }, status=200)
            else:
                return JsonResponse({
                    'success': False,
                    'error_message': 'Authentication failed after registration.'
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'errors': format_errors(form.errors)
            }, status=400)

    return JsonResponse({
        'success': False,
        'error_message': 'Register failed. Invalid method.'
    }, status=400)


# LogOut view to handle user logout
@csrf_protect
def logout(request):
    """
    Handles user logout and clears the session.

    Parameters:
    - POST request: The HTTP request

    Returns:
    - JsonResponse with boolean success or failure, and error message if needed.
    """
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error_message': 'Logout failed. Invalid method.'})


# Create checkout session for Stripe payment
@csrf_protect
def create_checkout_session(request):
    """
    Creates a new checkout session for Stripe payment, accepting fight details and seat selection.

    Parameters:
    - POST request: The HTTP request

    Returns:
    - JsonResponse with the checkout session URL if successful.
    - JsonResponse with an error message if an exception occurred.
    """
    if request.method == 'POST':
        user = request.user

        try:
            data = json.loads(request.body)

            line_items = []

            for seat in data['selectedSeats']:
                line_items.append({
                    'price': seat['priceId'],
                    'quantity': 1,
                })

            selected_services = data.get('selectedServices', {})
            for service_type in ['meals', 'baggage', 'comfort']:
                for service in selected_services.get(service_type, []):
                    line_items.append({
                        'price': service['priceId'],
                        'quantity': 1,
                    })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                customer_email=user.email,
                metadata={
                    'user_id': user.id,
                    'flight_id': data['flightId'],
                    'seats': json.dumps(data['selectedSeats']),
                    'services': json.dumps(data.get('selectedServices', {})),
                },
                success_url='http://localhost:8000/bookings/',
                cancel_url='http://localhost:8000/',
            )

            return JsonResponse({'url': session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


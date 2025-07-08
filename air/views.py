import json
import random
import string
from collections import defaultdict

import stripe
from dateutil import parser
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorDict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import LoginForm, RegisterForm
from .models import Flight, Ticket, TicketStatusChoices, Seats, Meal, Baggage, Comfort
from .utils import generate_booking_reference

stripe.api_key = settings.STRIPE_API_KEY


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
def generate_unique_username(base_username, User):
    """
    Generates a unique username based on the given base username.
    If the base username is already taken, appends a number and increments it until available.

    Parameters:
        base_username (str): The initial username to base the unique name on.

    Returns:
        str: A unique username that does not exist in the user model.
    """
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
    return ", ".join(seats)


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
    formatted_date = date_obj.strftime("%d.%m.%Y")
    formatted_time = date_obj.strftime("%H:%M")
    return f"{formatted_date} {formatted_time}"


# Home page with the list of flights
def index(request):
    """
    Renders the home page with Vue.js container

    Parameters:
    - GET request: The HTTP request

    Returns:
    - render: Renders the 'home.html' template with flight data and cities
    """
    flights = Flight.objects.all().order_by("destination", "departure_time")
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
        duration_str = f"{hours}h {minutes}m"

        seats_taken = list(
            Ticket.objects.filter(
                flight_id=flight.id, status=TicketStatusChoices.UPCOMING
            )
            .order_by("seat_number")
            .values_list("seat_number", flat=True)
        )

        flight_data[route].append(
            {
                "date": flight.departure_time.isoformat(),
                "flight_id": flight.id,
                "time": flight.departure_time.strftime("%d.%m.%Y at %H:%M"),
                "airline": "",
                "aircraft": "",
                "gate": "",
                "terminal": "",
                "duration": duration_str,
                "price": float(flight.base_price),
                "seats_total": seats_total,
                "seats_available": seats_available,
                "taken": seats_taken,
            }
        )

    return render(
        request,
        "home.html",
        {
            "flight_dates": dict(flight_data),
            "unique_cities": sorted(cities),
        },
    )


@login_required(login_url="/")
def bookings(request):
    if request.user.is_authenticated:
        return render(request, "bookings.html")


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
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                auth_login(request, user)
                return JsonResponse(
                    {
                        "success": True,
                        "user": {
                            "id": user.id,
                            "name": f"{user.first_name} {user.last_name}",
                            "email": user.email,
                        },
                    }
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "errors": {"general": "Невірний email або пароль"},
                    }
                )
        else:
            # Сконвертувати form.errors до простого словника
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors})

    return JsonResponse(
        {"success": False, "errors": {"general": "Login failed. Invalid method."}}
    )


@csrf_protect
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]

            # Перевіряємо унікальність email
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                return JsonResponse(
                    {
                        "success": False,
                        "errors": {"email": "Користувач з таким email вже існує."},
                    }
                )

            # Створюємо базове ім’я користувача
            base_username = email.split("@")[0]

            # Створюємо користувача
            user = form.save(commit=False)
            user.set_password(password)
            if User.objects.filter(username=base_username).exists():
                username = generate_unique_username(base_username, User)
                user.username = username
            else:
                user.username = base_username
            user.email = email
            user.save()

            # Аутентифікація
            user = authenticate(request, email=email, password=password)
            if user:
                user.backend = "air.backends.EmailBackend"
                auth_login(request, user)

                return JsonResponse(
                    {
                        "success": True,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "name": f"{user.first_name} {user.last_name}",
                        },
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error_message": "Authentication failed after registration.",
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {"success": False, "errors": format_errors(form.errors)}, status=400
            )

    return JsonResponse(
        {"success": False, "error_message": "Register failed. Invalid method."},
        status=400,
    )


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
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse({"success": True})
    return JsonResponse(
        {"success": False, "error_message": "Logout failed. Invalid method."}
    )


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
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    user = request.user

    try:
        data = json.loads(request.body)
        flight_id = data.get("flightId")
        selected_seats = data.get("selectedSeats", [])
        selected_services = data.get("selectedServices", {})

        line_items = []

        for seat in selected_seats:
            seat_number = seat.get("seatNumber")
            price_id = seat.get("priceId")

            try:
                db_seat = Seats.objects.get(flight_id=flight_id, seat_number=seat_number)
            except Seats.DoesNotExist:
                return JsonResponse({"error": f"Seat {seat_number} not found for this flight"}, status=400)

            if db_seat.stripe_price_id != price_id:
                return JsonResponse({"error": f"Invalid priceId for seat {seat_number}"}, status=400)

            line_items.append({
                "price": db_seat.stripe_price_id,
                "quantity": 1
            })

        def validate_service(model, service_name):
            for service in selected_services.get(service_name, []):
                price_id = service.get("priceId")
                try:
                    model.objects.get(stripe_price_id=price_id)
                except model.DoesNotExist:
                    return JsonResponse({"error": f"Invalid {service_name} priceId: {price_id}"}, status=400)

                line_items.append({
                    "price": price_id,
                    "quantity": 1
                })
            return None

        for model, key in [(Meal, "meals"), (Baggage, "baggage"), (Comfort, "comfort")]:
            response = validate_service(model, key)
            if response:
                return response

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            customer_email=user.email,
            metadata={
                "user_id": user.id,
                "flight_id": flight_id,
                "seats": json.dumps(selected_seats),
                "services": json.dumps(selected_services),
            },
            success_url="http://localhost:8000/bookings/",
            cancel_url="http://localhost:8000/",
        )

        return JsonResponse({
            "success": True,
            "data": {
                "url": session.url
            }
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "errors": {
                "non_field_error": str(e)
            }
        }, status=500)

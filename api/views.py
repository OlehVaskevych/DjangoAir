import json
import random
import string
from datetime import timedelta

import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication, SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from air.models import (AirlineUser, Airplane, Baggage, BoardingPass, CheckIn,
                        Comfort, Flight, Meal, Ticket, TicketStatusChoices, Seats)

from .serializers import (AirlineUserSerializer, AirplaneSerializer,
                          BaggageSerializer, BoardingPassSerializer,
                          CheckInSerializer, ComfortSerializer,
                          CurrentUserSerializer, FlightSerializer,
                          MealSerializer, TicketSerializer)


def generate_view_sets(model, model_serializer):
    return type(
        f"{model.__name__}ViewSet",
        (viewsets.ModelViewSet,),
        {"queryset": model.objects.all(), "serializer_class": model_serializer},
    )


AirlineUsersViewSet = generate_view_sets(AirlineUser, AirlineUserSerializer)
MealViewSet = generate_view_sets(Meal, MealSerializer)
BaggageViewSet = generate_view_sets(Baggage, BaggageSerializer)
ComfortViewSet = generate_view_sets(Comfort, ComfortSerializer)
TicketViewSet = generate_view_sets(Ticket, TicketSerializer)
CheckInViewSet = generate_view_sets(CheckIn, CheckInSerializer)
BoardingPassViewSet = generate_view_sets(BoardingPass, BoardingPassSerializer)


# Generates a booking reference like 'A1B2C3D4E5'
def generate_booking_reference():
    """
    Generates a random 10-character booking reference consisting of
    uppercase letters and digits.

    Returns:
    - str: A 10-character alphanumeric booking reference.
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


# Function to retrieve the current user`s information
class CurrentUserAPIView(APIView):
    """
    Checks if the user is authenticated and returns user information.

    Parameters:
    - request: The HTTP request

    Returns:
    - JsonResponse with the user`s information if authenticated.
    - JsonResponse with 'isAuthenticated': False if the user is not authenticated.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = CurrentUserSerializer(request.user)
            return Response(
                {
                    "isAuthenticated": True,
                    "user": serializer.data,
                }
            )
        return Response(
            {
                "isAuthenticated": False,
                "user": None,
            }
        )


# Returns a list of tickets for the currently authenticated user in JSON format
class UserTicketsAPIView(APIView):
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

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
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
        tickets = Ticket.objects.filter(passenger__id=user_id).select_related("flight")

        data = []
        for ticket in tickets:
            flight = ticket.flight

            data.append(
                {
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
                    "boardingTime": (
                        flight.departure_time - timedelta(minutes=30)
                    ).strftime("%H:%M"),
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
                                "dietaryOptions": [
                                    opt.name for opt in meal.dietary_options.all()
                                ],
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
                    },
                }
            )

        return Response(data)


class AdditionalServicesAPIView(APIView):
    @staticmethod
    def get(request):
        meals = Meal.objects.all()
        meals_data = MealSerializer(meals, many=True).data

        baggage_data = BaggageSerializer(Baggage.objects.all(), many=True).data
        comfort_data = ComfortSerializer(Comfort.objects.all(), many=True).data
        services_data = {
            "meals": meals_data,
            "baggage": baggage_data,
            "comfort": comfort_data,
        }

        return Response(services_data)


class CancelTicketAPIView(APIView):
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

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            print(data)
            ticket_id = data.get("ticket_id")

            if not ticket_id:
                return Response(
                    {"success": False, "error": "Missing ticket_id."}, status=400
                )

            ticket = Ticket.objects.get(id=ticket_id)

            if ticket.passenger != request.user:
                return Response(
                    {"success": False, "error": "Permission denied."}, status=403
                )

            ticket.status = TicketStatusChoices.CANCELED
            ticket.save()

            return Response({"status": "success"})

        except Ticket.DoesNotExist:
            return Response(
                {"success": False, "error": "Ticket not found."}, status=404
            )
        except json.JSONDecodeError:
            return Response({"success": False, "error": "Invalid JSON."}, status=400)


# Handles Stripe webhook event when a payment is successfully completed
@method_decorator(csrf_exempt, name="dispatch")
@authentication_classes([])
@permission_classes([])
class StripeWebhookView(APIView):
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

    @staticmethod
    def post(request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        if sig_header is None:
            print("Missing stripe signature header.")
            return Response(
                {"error": "Missing stripe signature header."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        except ValueError as e:
            print(f"⚠️ Invalid payload: {e}")
            return Response(
                {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
            )

        except stripe.error.SignatureVerificationError as e:
            print(f"⚠️ Invalid signature: {e}")
            return Response(
                {"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
            )

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            metadata = session.get("metadata", {})
            print(metadata)

            if "seats" not in metadata:
                print("⚠️ No seats found in metadata.")
                return Response(
                    {"error": "No seats in metadata"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                seats = json.loads(metadata.get("seats", "[]"))
                services = json.loads(metadata.get("services", "{}"))
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON Decode Error: {e}")
                return Response(
                    {"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
                )

            from .serializers import (AirplaneSerializer, BaggageSerializer,
                                      ComfortSerializer, MealSerializer,
                                      TicketSerializer)

            meal_ids = [m["id"] for m in services.get("meals", [])]
            baggage_ids = [b["id"] for b in services.get("baggage", [])]
            comfort_ids = [c["id"] for c in services.get("comfort", [])]

            meal_objs = Meal.objects.filter(id__in=meal_ids)
            baggage_objs = Baggage.objects.filter(id__in=baggage_ids)
            comfort_objs = Comfort.objects.filter(id__in=comfort_ids)

            gate = 1 if comfort_objs.filter(id=1).exists() else random.randint(2, 6)

            try:
                user = AirlineUser.objects.get(id=metadata["user_id"])
            except AirlineUser.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
                )

            for seat in seats:
                ticket = Ticket.objects.create(
                    seat_number=seat["id"],
                    price=seat["price"],
                    flight_id=metadata["flight_id"],
                    passenger_id=user.id,
                    seat_class=seat["class"],
                    booking_reference=generate_booking_reference(),
                    gate=gate,
                )

                ticket.meals.set(meal_objs)
                ticket.baggage.set(baggage_objs)
                ticket.comforts.set(comfort_objs)

                boarding_time = ticket.flight.departure_time - timedelta(minutes=30)

                subject = "Ваш квиток"
                context = {
                    "user": user,
                    "ticket": ticket,
                    "formatted_data": {
                        "date": ticket.flight.departure_time.strftime("%d.%m.%Y"),
                        "departure_time": ticket.flight.departure_time.strftime(
                            "%H:%M"
                        ),
                        "arrival_time": ticket.flight.arrival_time.strftime("%H:%M"),
                        "boarding_time": boarding_time.strftime("%H:%M"),
                    },
                }

                message_html = render_to_string("ticket_email.html", context)

                send_mail(
                    subject=subject,
                    message="Ваш email-клієнт не підтримує HTML.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    html_message=message_html,
                )

        return Response(status=status.HTTP_200_OK)


class SeatMapAPIView(APIView):
    def get(self, request, flight_id):
        seats = Seats.objects.filter(flight_id=flight_id)

        if not seats.exists():
            return Response({"seatMap": []}, status=status.HTTP_200_OK)

        seat_map_dict = {}

        for seat in seats:
            try:
                row_number = int(''.join(filter(str.isdigit, seat.seat_number)))
                seat_letter = ''.join(filter(str.isalpha, seat.seat_number)).upper()
            except (ValueError, TypeError):
                continue

            seat_number = f"{row_number}{seat_letter}"

            if row_number not in seat_map_dict:
                seat_map_dict[row_number] = {
                    "row": row_number,
                    "seats": [],
                    "class": seat.seat_class,
                    "stripe_price_id": seat.stripe_price_id,
                    "occupied_seats": []
                }

            if seat_letter not in seat_map_dict[row_number]["seats"]:
                seat_map_dict[row_number]["seats"].append(seat_letter)

            if seat.is_reserved:
                seat_map_dict[row_number]["occupied_seats"].append(seat_number)

        # Сортуємо літери всередині кожного ряду
        for row in seat_map_dict.values():
            row["seats"].sort()
            row["occupied_seats"].sort()

        # Перетворити словник у список і відсортувати по номеру ряду
        seat_map = [seat_map_dict[row] for row in sorted(seat_map_dict.keys())]

        return Response({"seatMap": seat_map}, status=status.HTTP_200_OK)

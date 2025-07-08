import string

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from .utils import generate_unique_booking_reference, generate_booking_reference, get_random_gate


class DietaryOption(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name of the food option")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dietary Option"
        verbose_name_plural = "Dietary Options"


class SeatClassChoices(models.TextChoices):
    ECONOMY = "economy", "Economy"
    BUSINESS = "business", "Business"
    FIRST = "first", "First"


class TicketStatusChoices(models.TextChoices):
    UPCOMING = "upcoming", "Upcoming"
    CANCELED = "canceled", "Canceled"
    BOARDED = "boarded", "Boarded"
    CHECKED_IN = "checked_in", "Checked In"
    LATE = "late", "Late"
    USED = "used", "Used"


class FlightStatusChoices(models.TextChoices):
    UPCOMING = "upcoming", "Upcoming"
    CANCELED = "canceled", "Canceled"
    IN_AIR = "in_air", "In Air"
    ARRIVED = "arrived", "Arrived"


class AirlineUser(AbstractUser):
    class Role(models.TextChoices):
        PASSENGER = "passenger", "Passenger"
        GATE_MANAGER = "gate_manager", "Gate Manager"
        CHECKIN_MANAGER = "checkin_manager", "Check-in Manager"
        SUPERVISOR = "supervisor", "Supervisor"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PASSENGER,
        verbose_name="User Role",
        help_text="Defines the user role in the airline system",
    )

    class Meta:
        verbose_name = "Airline User"
        verbose_name_plural = "Airline Users"


class Meal(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Meal name",
        help_text="Name of the meal",
    )
    description = models.TextField(
        verbose_name="Meal description",
        help_text="Description of the meal",
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Meal price",
        help_text="Price of the meal",
    )
    image_url = models.URLField(
        verbose_name="Meal image URL",
        help_text="Image url of the meal",
    )
    dietary_options = models.ManyToManyField(
        DietaryOption,
        related_name="meals",
        verbose_name="Dietary Options",
    )
    stripe_price_id = models.CharField(
        max_length=100,
        verbose_name="Stripe price ID",
        help_text="Stripe price id for payment",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Meal"
        verbose_name_plural = "Meals"


class Baggage(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Baggage name",
        help_text="Name of the baggage",
    )
    description = models.TextField(
        verbose_name="Baggage description",
        help_text="Description of the baggage",
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Baggage price",
        help_text="Price of the baggage",
    )
    weight = models.FloatField(
        verbose_name="Baggage weight",
        help_text="Weight of the baggage",
    )
    stripe_price_id = models.CharField(
        max_length=100,
        verbose_name="Stripe price ID",
        help_text="Stripe price id for payment",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Baggage"
        verbose_name_plural = "Baggages"


class Comfort(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Comfort option name",
        help_text="Name of the comfort option",
    )
    description = models.TextField(
        verbose_name="Comfort option description",
        help_text="Description of the comfort option",
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Comfort option price",
        help_text="Price of the comfort option",
    )
    stripe_price_id = models.CharField(
        max_length=100,
        verbose_name="Stripe price ID",
        help_text="Stripe price id for payment",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Comfort"
        verbose_name_plural = "Comforts"


class Airplane(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Airplane name",
        help_text="Name of the airplane",
    )
    seat_capacity = models.PositiveIntegerField(
        verbose_name="Airplane seat capacity",
        help_text="Seat capacity of the airplane",
    )
    economy_seats = models.PositiveIntegerField(
        default=0,
        verbose_name="Airplane economy seats",
        help_text="Seat capacity of the airplane",
    )
    business_seats = models.PositiveIntegerField(
        default=0,
        verbose_name="Airplane business seats",
        help_text="Seat capacity of the airplane",
    )
    first_class_seats = models.PositiveIntegerField(
        default=0,
        verbose_name="Airplane first class seats",
        help_text="Seat capacity of the airplane",
    )

    def __str__(self):
        return f"{self.name} ({self.seat_capacity} seats)"

    class Meta:
        verbose_name = "Airplane"
        verbose_name_plural = "Airplanes"


class Seats(models.Model):
    class SeatClassPriceID(models.TextChoices):
        ECONOMY_PRICE = "price_1RP0yYQMzydK9SUprJfIiJYw", "Economy price"
        BUSINESS_PRICE = "price_1RP0yyQMzydK9SUpQVDc8Xlz", "Business price"
        FIRSTCLASS_PRICE = "price_1RP0zFQMzydK9SUptZsV3qKC", "First class price"


    flight = models.ForeignKey(
        "Flight", on_delete=models.CASCADE, verbose_name="seats"
    )
    seat_number = models.CharField(
        max_length=10,
        choices=SeatClassChoices.choices,
        default=SeatClassChoices.ECONOMY,
    )
    stripe_price_id = models.CharField(
        max_length=100,
        verbose_name="Stripe price ID",
        choices=SeatClassPriceID.choices,
        default=SeatClassPriceID.ECONOMY_PRICE,
    )
    is_reserved = models.BooleanField(default=False, verbose_name="Is reserved")


class Flight(models.Model):
    flight_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Flight number",
        help_text="Unique flight number",
        db_index=True,
    )
    origin = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Origin",
        help_text="Origin of the flight",
    )
    destination = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Destination",
        help_text="Destination of the flight",
    )
    origin_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Origin code",
        help_text="Origin code of the flight",
    )
    destination_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Destination code",
        help_text="Destination code of the flight",
    )
    departure_time = models.DateTimeField(
        verbose_name="Departure time",
        help_text="Departure time of the flight",
    )
    arrival_time = models.DateTimeField(
        verbose_name="Arrival time",
        help_text="Arrival time of the flight",
    )
    base_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Base price",
        help_text="Base price (without services)",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
        null=True,
        blank=True,
        verbose_name="Airplane",
        help_text="Airplane of the flight",
    )
    status = models.CharField(
        choices=FlightStatusChoices.choices,
        blank=False,
        null=False,
        default=FlightStatusChoices.UPCOMING,
        verbose_name="Status",
        help_text="Status of the flight",
    )

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"

    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"


class Ticket(models.Model):
    passenger = models.ForeignKey(
        AirlineUser,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Passenger",
        help_text="Passenger of the ticket",
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Flight",
        help_text="Flight of the ticket",
    )
    seat_number = models.CharField(
        max_length=5,
        verbose_name="Seat number",
        help_text="Seat number of the ticket",
    )
    seat_class = models.CharField(
        max_length=20,
        choices=SeatClassChoices.choices,
        default=SeatClassChoices.ECONOMY,
        verbose_name="Seat class",
        help_text="Seat class of the ticket",
    )
    gate = models.IntegerField(
        default=get_random_gate,
        blank=False,
        null=False,
        verbose_name="Gate",
        help_text="Gate of the ticket",
    )
    meals = models.ManyToManyField(
        Meal,
        related_name="tickets",
        blank=True,
        verbose_name="Meals",
        help_text="Meals of the ticket",
    )
    baggage = models.ManyToManyField(
        Baggage,
        related_name="tickets",
        blank=True,
        verbose_name="Baggage options",
        help_text="Baggage options of the ticket",
    )
    comforts = models.ManyToManyField(
        Comfort,
        related_name="tickets",
        blank=True,
        verbose_name="Comfort options",
        help_text="Comfort options of the ticket",
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Price",
        help_text="Price of the ticket",
    )
    is_checked_in = models.BooleanField(
        default=False,
        verbose_name="Is passenger checked in",
        help_text="Is passenger checked in",
    )
    is_boarded = models.BooleanField(
        default=False,
        verbose_name="Is passenger boarded",
        help_text="Is passenger boarded",
    )
    booking_reference = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        default=generate_booking_reference,
        verbose_name="Booking reference",
        help_text="Booking reference of the ticket",
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
        help_text="Ticket creating time",
    )
    status = models.CharField(
        max_length=20,
        choices=TicketStatusChoices.choices,
        default=TicketStatusChoices.UPCOMING,
        verbose_name="Status",
        help_text="Status of the ticket",
    )
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = generate_unique_booking_reference()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} | {self.passenger.username} | {self.flight.flight_number}"

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"


class CheckIn(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="checkins",
        verbose_name="Ticket",
        help_text="Ticket of the checkin",
    )
    luggage_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Luggage weight",
        help_text="Luggage weight of the ticket",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check-in for {self.ticket.booking_reference}"

    class Meta:
        verbose_name = "Check-in"
        verbose_name_plural = "Check-ins"


class BoardingPass(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="boarding_pass",
        verbose_name="Ticket",
        help_text="Ticket of the boarding pass",
    )
    gate_number = models.CharField(
        max_length=10,
        verbose_name="Gate number",
        help_text="Gate number of the boarding pass",
    )
    boarding_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Boarding time",
        help_text="Boarding time of the boarding pass",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Boarding Pass {self.ticket.booking_reference} @ Gate {self.gate_number}"
        )

    class Meta:
        verbose_name = "Boarding Pass"
        verbose_name_plural = "Boarding Passes"

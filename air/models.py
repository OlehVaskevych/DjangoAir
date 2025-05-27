from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string

def generate_booking_reference():
    # Генерація випадкового рядка з букв і цифр довжиною 10 символів
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class DietaryOption(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SeatClassChoices(models.TextChoices):
    ECONOMY = 'economy', 'Economy'
    BUSINESS = 'business', 'Business'
    FIRST = 'first', 'First'

class TicketStatusChoices(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    CANCELED = 'canceled', 'Canceled'
    BOARDED = 'boarded', 'Boarded'
    CHECKED_IN = 'checked_in', 'Checked In'
    LATE = 'late', 'Late'
    USED = 'used', 'Used'

class FlightStatusChoices(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    CANCELED = 'canceled', 'Canceled'
    IN_AIR = 'in_air', 'In Air'
    ARRIVED = 'arrived', 'Arrived'


class AirlineUser(AbstractUser):
    class Role(models.TextChoices):
        PASSENGER = 'passenger', 'Passenger'
        GATE_MANAGER = 'gate_manager', 'Gate Manager'
        CHECKIN_MANAGER = 'checkin_manager', 'Check-in Manager'
        SUPERVISOR = 'supervisor', 'Supervisor'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PASSENGER,
    )

    def save(self, *args, **kwargs):
        if self.role in [
            AirlineUser.Role.SUPERVISOR,
            AirlineUser.Role.GATE_MANAGER,
            AirlineUser.Role.CHECKIN_MANAGER
        ]:
            self.is_staff = True
            self.is_superuser = (self.role == AirlineUser.Role.SUPERVISOR)
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

class Meal(models.Model):
    name = models.CharField(
        max_length=100,
        help_text='Name of the meal',
    )
    description = models.TextField(
        help_text='Description of the meal',
    )
    price = models.FloatField(
        help_text='Price of the meal',
    )
    image_url = models.URLField(
        help_text='Image url of the meal',
    )
    dietary_options = models.ManyToManyField(
        DietaryOption,
        related_name='meals',
    )
    stripe_price_id = models.CharField(
        max_length=100,
        help_text='Stripe price id for payment',
    )

    def __str__(self):
        return self.name

class Baggage(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        help_text='Description of the baggage',
    )
    price = models.FloatField(
        help_text='Price of the baggage',
    )
    weight = models.FloatField(
        help_text='Weight of the baggage',
    )
    stripe_price_id = models.CharField(
        max_length=100,
        help_text='Stripe price id for payment',
    )

class Comfort(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    price = models.FloatField()
    stripe_price_id = models.CharField(
        max_length=100,
        help_text='Stripe price id for payment',
    )


class Airplane(models.Model):
    name = models.CharField(
        max_length=100,
        help_text='Name of the airplane',
    )
    seat_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.seat_capacity} seats)"


class Flight(models.Model):
    flight_number = models.CharField(
        max_length=10,
        unique=True,
        help_text='Unique flight number',
    )
    origin = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    destination = models.CharField(max_length=100)
    origin_code = models.CharField(max_length=10, blank=True)
    destination_code = models.CharField(max_length=10, blank=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    base_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Base price (without services)',
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name='flights',
        null=True,
        blank=True,
    )
    status = models.CharField(
        choices=FlightStatusChoices.choices,
        blank=False,
        null=False,
        default=FlightStatusChoices.UPCOMING,
    )

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"


class Ticket(models.Model):
    passenger = models.ForeignKey(
        AirlineUser,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    seat_number = models.CharField(max_length=5)
    seat_class = models.CharField(
        max_length=20,
        choices=SeatClassChoices.choices,
        default=SeatClassChoices.ECONOMY
    )
    gate = models.IntegerField(
        default=random.randint(2, 6),
        blank=False,
        null=False,
    )
    meals = models.ManyToManyField(
        Meal,
        related_name='tickets',
        blank=True
    )
    baggage = models.ManyToManyField(
        Baggage,
        related_name='tickets',
        blank=True
    )
    comforts = models.ManyToManyField(
        Comfort,
        related_name='tickets',
        blank=True
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_checked_in = models.BooleanField(default=False)
    is_boarded = models.BooleanField(default=False)
    booking_reference = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        default=generate_booking_reference(),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(
        max_length=20,
        choices=TicketStatusChoices.choices,
        default=TicketStatusChoices.UPCOMING,
    )

    def __str__(self):
        return f"{self.booking_reference} | {self.passenger.username} | {self.flight.flight_number}"


class CheckIn(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='checkins'
    )
    luggage_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check-in for {self.ticket.booking_reference}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.ticket.is_checked_in = True
        self.ticket.status = TicketStatusChoices.CHECKED_IN
        self.ticket.save(update_fields=['is_checked_in', 'status'])


class BoardingPass(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='boarding_pass'
    )
    gate_number = models.CharField(max_length=10)
    boarding_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boarding Pass {self.ticket.booking_reference} @ Gate {self.gate_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.ticket.is_boarded = True
        self.ticket.status = TicketStatusChoices.BOARDED
        self.ticket.save(update_fields=['is_boarded', 'status'])

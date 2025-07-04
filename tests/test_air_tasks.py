import pytest
from django.utils import timezone
from datetime import timedelta

from air.tasks import update_flight_status
from air.models import (
    Flight,
    FlightStatusChoices,
    TicketStatusChoices,
    Ticket,
    AirlineUser
)

@pytest.mark.django_db
def test_update_flight_status():
    now = timezone.now()

    user1 = AirlineUser.objects.create(
        username="user1",
        email="user1@example.com",
        password="password123"
    )
    user2 = AirlineUser.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='password2'
    )

    # Створюємо два польоти з унікальним flight_number
    flight_upcoming = Flight.objects.create(
        flight_number="AB1234",
        departure_time=now - timedelta(hours=1),
        arrival_time=now + timedelta(hours=1),
        status=FlightStatusChoices.UPCOMING,
        base_price=100.0,
        origin="LAX",
        destination="JFK"
    )

    flight_in_air = Flight.objects.create(
        flight_number="CD5678",
        departure_time=now - timedelta(hours=3),
        arrival_time=now - timedelta(minutes=1),
        status=FlightStatusChoices.IN_AIR,
        base_price=150.0,
        origin="LAX",
        destination="JFK"
    )

    # Створюємо квитки для користувачів, пов'язані з польотом
    ticket1 = Ticket.objects.create(
        flight=flight_upcoming,
        passenger=user1,
        seat_number='12A',
        status=TicketStatusChoices.UPCOMING,
        is_checked_in=True,
        is_boarded=True,
        price=200.0,
    )

    ticket2 = Ticket.objects.create(
        flight=flight_upcoming,
        passenger=user2,
        seat_number='12B',
        status=TicketStatusChoices.UPCOMING,
        is_checked_in=False,
        is_boarded=False,
        price=200.0,
    )

    update_flight_status()

    # Перевіряємо оновлення статусів польотів
    flight_upcoming.refresh_from_db()
    flight_in_air.refresh_from_db()
    assert flight_upcoming.status == FlightStatusChoices.IN_AIR
    assert flight_in_air.status == FlightStatusChoices.ARRIVED

    # Перевіряємо оновлення статусів квитків
    ticket1.refresh_from_db()
    ticket2.refresh_from_db()

    assert ticket1.status == TicketStatusChoices.USED  # бо is_checked_in=True і is_boarded=True
    assert ticket2.status == TicketStatusChoices.LATE  # бо не пройшли чек-ін і посадку
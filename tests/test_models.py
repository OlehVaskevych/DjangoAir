import pytest
from django.utils import timezone

from air.models import (AirlineUser, Airplane, Baggage, BoardingPass, CheckIn,
                        Comfort, DietaryOption, Flight, Meal, SeatClassChoices,
                        Ticket, TicketStatusChoices)


@pytest.mark.django_db
def test_dietary_option_str():
    option = DietaryOption.objects.create(name="Vegan")
    assert str(option) == "Vegan"


@pytest.mark.django_db
def test_airline_user_save_sets_staff_flags():
    user = AirlineUser(username="user1", role=AirlineUser.Role.PASSENGER)
    user.save()
    assert user.is_staff is False
    assert user.is_superuser is False

    gm = AirlineUser(username="gate_manager", role=AirlineUser.Role.GATE_MANAGER)
    gm.save()
    assert gm.is_staff is True
    assert gm.is_superuser is False

    ci = AirlineUser(username="check-in_manager", role=AirlineUser.Role.CHECKIN_MANAGER)
    ci.save()
    assert ci.is_staff is True
    assert ci.is_superuser is False

    supervisor = AirlineUser(username="supervisor", role=AirlineUser.Role.SUPERVISOR)
    supervisor.save()
    assert supervisor.is_staff is True
    assert supervisor.is_superuser is True


@pytest.mark.django_db
def test_meal_str_and_m2m_dietary_options():
    meal = Meal.objects.create(
        name="Chicken Sandwich",
        description="Tasty chicken sandwich",
        price=10.5,
        image_url="https://example.com/img.jpg",
        stripe_price_id="price_123",
    )
    vegan = DietaryOption.objects.create(name="Vegan")
    gluten_free = DietaryOption.objects.create(name="Gluten Free")
    meal.dietary_options.add(vegan, gluten_free)
    meal.refresh_from_db()
    assert str(meal) == "Chicken Sandwich"

    assert vegan in meal.dietary_options.all()
    assert gluten_free in meal.dietary_options.all()


@pytest.mark.django_db
def test_baggage_str():
    baggage = Baggage.objects.create(
        name="Extra Bag",
        description="Extra baggage",
        price=50.0,
        weight=10.0,
        stripe_price_id="price_456",
    )
    assert str(baggage) == "Extra Bag"


@pytest.mark.django_db
def test_comfort_str():
    comfort = Comfort.objects.create(
        name="Extra Legroom",
        description="More space for legs",
        price=20.0,
        stripe_price_id="price_789",
    )
    assert str(comfort) == "Extra Legroom"


@pytest.mark.django_db
def test_airplane_str():
    airplane = Airplane.objects.create(name="Boeing 737", seat_capacity=180)
    assert str(airplane) == "Boeing 737 (180 seats)"


@pytest.mark.django_db
def test_flight_str():
    airplane = Airplane.objects.create(name="Boeing 737", seat_capacity=180)
    flight = Flight.objects.create(
        flight_number="AB123",
        origin="Kyiv",
        destination="London",
        origin_code="KBP",
        destination_code="LHR",
        departure_time=timezone.now(),
        arrival_time=timezone.now(),
        base_price=100,
        airplane=airplane,
        status="upcoming",
    )
    assert str(flight) == "AB123: Kyiv → London"


@pytest.mark.django_db
def test_ticket_str_and_m2m_relations():
    user = AirlineUser.objects.create_user(username="passenger", password="pass")
    airplane = Airplane.objects.create(name="Boeing 737", seat_capacity=180)
    flight = Flight.objects.create(
        flight_number="CD456",
        origin="Paris",
        destination="Berlin",
        departure_time=timezone.now(),
        arrival_time=timezone.now(),
        base_price=150,
        airplane=airplane,
        status="upcoming",
    )
    ticket = Ticket.objects.create(
        passenger=user,
        flight=flight,
        seat_number="12A",
        seat_class=SeatClassChoices.ECONOMY,
        price=200,
        status=TicketStatusChoices.UPCOMING,
    )
    meal = Meal.objects.create(
        name="Salad",
        description="Fresh salad",
        price=5,
        image_url="https://example.com/salad.jpg",
        stripe_price_id="price_salad",
    )
    baggage = Baggage.objects.create(
        name="Small Bag",
        description="Small baggage",
        price=15,
        weight=5,
        stripe_price_id="price_baggage",
    )
    comfort = Comfort.objects.create(
        name="Window Seat",
        description="Seat near window",
        price=10,
        stripe_price_id="price_comfort",
    )
    ticket.meals.add(meal)
    ticket.baggage.add(baggage)
    ticket.comforts.add(comfort)

    ticket.refresh_from_db()
    assert meal in ticket.meals.all()
    assert baggage in ticket.baggage.all()
    assert comfort in ticket.comforts.all()
    # booking_reference автоматично згенеровано і має довжину 10
    assert len(ticket.booking_reference) == 10
    assert str(ticket).startswith(ticket.booking_reference)


@pytest.mark.django_db
def test_checkin_save_updates_ticket_status():
    user = AirlineUser.objects.create_user(username="checkin_user", password="pass")
    flight = Flight.objects.create(
        flight_number="EF789",
        origin="NY",
        destination="LA",
        departure_time=timezone.now(),
        arrival_time=timezone.now(),
        base_price=300,
        status="upcoming",
    )
    ticket = Ticket.objects.create(
        passenger=user,
        flight=flight,
        seat_number="1B",
        seat_class=SeatClassChoices.BUSINESS,
        price=400,
        status=TicketStatusChoices.UPCOMING,
    )
    checkin = CheckIn.objects.create(ticket=ticket, luggage_weight=20)
    ticket.refresh_from_db()
    assert ticket.is_checked_in is True
    assert ticket.status == TicketStatusChoices.CHECKED_IN
    assert str(checkin) == f"Check-in for {ticket.booking_reference}"


@pytest.mark.django_db
def test_boarding_passes_save_updates_ticket_status():
    user = AirlineUser.objects.create_user(username="boarding_user", password="pass")
    flight = Flight.objects.create(
        flight_number="GH012",
        origin="Rome",
        destination="Milan",
        departure_time=timezone.now(),
        arrival_time=timezone.now(),
        base_price=120,
        status="upcoming",
    )
    ticket = Ticket.objects.create(
        passenger=user,
        flight=flight,
        seat_number="2C",
        seat_class=SeatClassChoices.FIRST,
        price=500,
        status=TicketStatusChoices.UPCOMING,
    )
    boarding_pass = BoardingPass.objects.create(ticket=ticket, gate_number="G5")
    ticket.refresh_from_db()
    assert ticket.is_boarded is True
    assert ticket.status == TicketStatusChoices.BOARDED
    assert str(boarding_pass) == f"Boarding Pass {ticket.booking_reference} @ Gate G5"

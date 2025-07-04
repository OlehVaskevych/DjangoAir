import json
from ctypes import pythonapi

from datetime import timedelta

import pytest
from unittest.mock import patch

from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from air.models import (
    AirlineUser, Flight, Ticket, Meal, Baggage, Comfort,
    TicketStatusChoices, CheckIn, BoardingPass
)

@pytest.mark.django_db
@patch("stripe.Webhook.construct_event")
@patch("api.views.send_mail")
def test_stripe_webhook_ticket_creation(mock_send_mail, mock_construct_event):
    client = APIClient()

    user = AirlineUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='securepassword'
    )

    flight = Flight.objects.create(
        flight_number="XY1234",
        origin="LAX",
        destination="JFK",
        origin_code="LAX",
        destination_code="JFK",
        departure_time="2099-01-01T15:00:00Z",
        arrival_time="2099-01-01T19:00:00Z",
        status="upcoming",
        base_price=100.0
    )

    meal = Meal.objects.create(name="Vegan", price=10.0)
    baggage = Baggage.objects.create(name="Large Bag", weight=20, price=15.0)
    comfort = Comfort.objects.create(name="Extra Legroom", description="Spacious seat", price=20.0)

    metadata = {
        "user_id": str(user.id),
        "flight_id": str(flight.id),
        "seats": json.dumps([{"id": "12A", "price": "150.0", "class": "economy"}]),
        "services": json.dumps({
            "meals": [{"id": meal.id}],
            "baggage": [{"id": baggage.id}],
            "comfort": [{"id": comfort.id}]
        })
    }

    payload = json.dumps({
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": metadata
            }
        }
    })

    # Mock signature validation
    mock_construct_event.return_value = json.loads(payload)

    url = reverse("succeed_payment")
    response = client.post(
        url,
        data=payload,
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test_signature"
    )

    # Assertions
    assert response.status_code == 200
    assert Ticket.objects.count() == 1

    ticket = Ticket.objects.first()
    assert ticket.passenger == user
    assert ticket.flight == flight
    assert ticket.seat_number == "12A"
    assert ticket.meals.first().id == meal.id
    assert ticket.baggage.first().id == baggage.id
    assert ticket.comforts.first().id == comfort.id

    # Перевірка надсилання email
    mock_send_mail.assert_called_once()

@pytest.mark.django_db
def test_cancel_ticket_success():
    user = AirlineUser.objects.create_user(
        email='test@example.com',
        password='password123',
        username='testuser'
    )

    flight = Flight.objects.create(
        flight_number="UA123",
        origin="Kyiv",
        destination="Lviv",
        origin_code="KBP",
        destination_code="LWO",
        departure_time="2030-01-01T12:00:00Z",
        arrival_time="2030-01-01T14:00:00Z",
        base_price=100
    )

    ticket = Ticket.objects.create(
        flight=flight,
        passenger=user,
        seat_number="12A",
        price=100,
        seat_class="Economy",
        status=TicketStatusChoices.UPCOMING,
        booking_reference="TESTREF123",
        gate=5
    )

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("cancel_ticket")

    response = client.post(url, {"ticket_id": ticket.id}, format="json")
    assert response.status_code == 200
    assert response.data["status"] == "success"
    ticket.refresh_from_db()
    assert ticket.status == TicketStatusChoices.CANCELED


@pytest.mark.django_db
def test_cancel_ticket_not_found():
    user = AirlineUser.objects.create_user(
        email='test@example.com',
        password='password123',
        username='testuser'
    )

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("cancel_ticket")

    response = client.post(url, {"ticket_id": 9999}, format="json")  # неіснуючий квиток
    assert response.status_code == 404
    assert response.data["success"] is False
    assert "Ticket not found" in response.data["error"]


@pytest.mark.django_db
def test_cancel_ticket_missing_ticket_id():
    user = AirlineUser.objects.create_user(
        email='test@example.com',
        password='password123',
        username='testuser'
    )

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("cancel_ticket")

    response = client.post(url, {}, format="json")  # без ticket_id
    assert response.status_code == 400
    assert response.data["success"] is False
    assert "Missing ticket_id" in response.data["error"]


@pytest.mark.django_db
def test_cancel_ticket_unauthenticated():
    client = APIClient()
    url = reverse("cancel_ticket")
    response = client.post(url, {"ticket_id": 1}, format="json")
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_additional_services_api():
    meal = Meal.objects.create(name="Vegan Meal", price=10.5, image_url='vegan.jpg')
    baggage = Baggage.objects.create(name="Extra Baggage", weight=20, price=15)
    comfort = Comfort.objects.create(name="Extra Legroom", description="More space", price=25)

    client = APIClient()
    url = reverse("additional_services")

    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert "meals" in data
    assert "baggage" in data
    assert "comfort" in data

@pytest.mark.django_db
def test_user_tickets_view_unauthenticated():
    client = APIClient()
    url = reverse('get_tickets')
    response = client.get(url)

    assert response.status_code == 401
    assert response.json()['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_user_tickets_view_authenticated():
    user = AirlineUser.objects.create_user(username='testuser', email='test@example.com', password='password123')

    # Створення об'єктів
    flight = Flight.objects.create(
        flight_number="XY123",
        origin="Lviv",
        destination="Kyiv",
        origin_code="LWO",
        destination_code="IEV",
        departure_time=timezone.now() + timedelta(days=1),
        arrival_time=timezone.now() + timedelta(days=1, hours=1),
        base_price=100,
    )

    ticket = Ticket.objects.create(
        flight=flight,
        passenger=user,
        seat_number="12A",
        seat_class="Economy",
        status="UPCOMING",
        price=100,
        gate=3,
    )

    # Додаткові сервіси
    meal = Meal.objects.create(name="Sandwich", price=10, image_url="img.jpg")
    baggage = Baggage.objects.create(name="Big Bag", weight=20, price=15)
    comfort = Comfort.objects.create(name="Extra Legroom", description="More space", price=25)

    ticket.meals.add(meal)
    ticket.baggage.add(baggage)
    ticket.comforts.add(comfort)

    # Аутентифікація
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('get_tickets')

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    ticket_data = data[0]
    assert ticket_data["flightNumber"] == "XY123"
    assert ticket_data["passengerName"] == f"{user.first_name} {user.last_name}"
    assert ticket_data["seats"][0]["id"] == "12A"
    assert "meals" in ticket_data["additional_services"]
    assert "baggage" in ticket_data["additional_services"]
    assert "comforts" in ticket_data["additional_services"]

@pytest.mark.django_db
def test_current_user_view_authenticated():
    client = APIClient()
    user = AirlineUser.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    client.force_authenticate(user=user)

    url = reverse("current_user")
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["isAuthenticated"] is True
    assert data["user"]["id"] == user.id
    assert data["user"]["name"] == user.first_name + " " + user.last_name
    assert data["user"]["email"] == 'test@example.com'
    assert data["user"]["role"] == user.role

@pytest.mark.django_db
def test_current_user_view_unauthenticated():
    client = APIClient()
    url = reverse("current_user")
    response = client.get(url)

    assert response.status_code == 401

# Мапінг моделей до їх url names у роутингу, адаптуй під свій роутінг
viewsets_info = [
    ("airlineuser-list", {"model": AirlineUser, "serializer_fields": ["email", "username"], "create_data": {"email": "test1@example.com", "username": "user1", "password": "testpass123"}}),
    ("meal-list", {"model": Meal, "serializer_fields": ["name"], "create_data": {"name": "Test Meal", "price": 10.0, "description": "Test Meal", "stripe_price_id": 'price_123'}}),
    ("baggage-list", {"model": Baggage, "serializer_fields": ["name"], "create_data": {"name": "Small Bag", "weight": 5, "price": 15.0, "description": "Test Baggage", "stripe_price_id": 'price_123'}}),
    ("comfort-list", {"model": Comfort, "serializer_fields": ["name"], "create_data": {"name": "Extra Legroom", "description": "More space", "price": 30.0, "stripe_price_id": 'price_123'}}),
    ("ticket-list", {"model": Ticket, "serializer_fields": ["seat_number", "price"], "create_data": {"seat_number": "12A", "price": 100.0}}),
    ("checkin-list", {"model": CheckIn, "serializer_fields": ["id"], "create_data": {"luggage_weight": 10, "created_at": timezone.now()}}),  # Потрібно доповнити дані, якщо є обов'язкові поля
    ("boardingpass-list", {"model": BoardingPass, "serializer_fields": ["id"], "create_data": {'gate_number': 1}}),  # Аналогічно
]

@pytest.mark.django_db
@pytest.mark.parametrize("url_name, info", viewsets_info)
def test_viewset_list_and_create(url_name, info):
    client = APIClient()

    # Створюємо базових користувача і політ (у разі потреби)
    user = AirlineUser.objects.create_user(
        email='user@example.com',
        password='password123',
        username='testuser'
    )

    flight = Flight.objects.create(
        flight_number="FL123",
        origin="Kyiv",
        destination="Lviv",
        origin_code="KBP",
        destination_code="LWO",
        departure_time=timezone.now() + timedelta(hours=2),
        arrival_time=timezone.now() + timedelta(hours=4),
        base_price=100.0
    )

    # GET list
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # POST create
    create_data = info["create_data"].copy()
    # Якщо потрібна авторизація - додай її тут:
    # user = AirlineUser.objects.create_user(...)
    # client.force_authenticate(user=user)

    model = info["model"]
    if model == Ticket:
        create_data["passenger"] = user.id
        create_data["flight"] = flight.id
    elif model == CheckIn:
        ticket = Ticket.objects.create(
            seat_number="15C",
            price=120.0,
            passenger=user,
            flight=flight,
            seat_class="Economy",
            booking_reference="ABC123",
            gate=3
        )
        create_data["ticket"] = ticket.id
    elif model == BoardingPass:
        ticket = Ticket.objects.create(
            seat_number="16D",
            price=150.0,
            passenger=user,
            flight=flight,
            seat_class="Economy",
            booking_reference="XYZ789",
            gate=4
        )
        create_data["ticket"] = ticket.id

    # Авторизація, якщо потрібно
    client.force_authenticate(user=user)

    response = client.post(url, create_data, format='json')
    print(f"{url_name} POST response:", response.json())

    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_405_METHOD_NOT_ALLOWED]

    if response.status_code == status.HTTP_201_CREATED:
        data = response.json()
        for field in info["serializer_fields"]:
            assert field in data

# Приклад для тестування деталізації (GET detail)
@pytest.mark.django_db
@pytest.mark.parametrize("url_name, info", viewsets_info)
def test_viewset_retrieve(url_name, info):
    client = APIClient()
    model = info["model"]
    create_data = info["create_data"].copy()

    # Динамічна підготовка залежностей
    if model == Ticket:
        user = AirlineUser.objects.create_user(email="u@example.com", username="user", password="1234")
        flight = Flight.objects.create(
            flight_number="F123",
            origin="Kyiv",
            destination="Lviv",
            origin_code="KBP",
            destination_code="LWO",
            departure_time=timezone.now() + timezone.timedelta(hours=1),
            arrival_time=timezone.now() + timezone.timedelta(hours=2),
            base_price=100.0,
        )
        create_data["passenger"] = user
        create_data["flight"] = flight

    elif model == CheckIn:
        user = AirlineUser.objects.create_user(email="checkin@example.com", username="checkuser", password="1234")
        flight = Flight.objects.create(
            flight_number="CHK123",
            origin="A",
            destination="B",
            origin_code="A1",
            destination_code="B2",
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=1),
            base_price=50.0,
        )
        ticket = Ticket.objects.create(
            seat_number="22C",
            price=100,
            passenger=user,
            flight=flight
        )
        create_data["ticket"] = ticket

    elif model == BoardingPass:
        user = AirlineUser.objects.create_user(email="b@example.com", username="bpuser", password="1234")
        flight = Flight.objects.create(
            flight_number="BP123",
            origin="X",
            destination="Y",
            origin_code="X1",
            destination_code="Y2",
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=1),
            base_price=70.0,
        )
        ticket = Ticket.objects.create(
            seat_number="15A",
            price=80,
            passenger=user,
            flight=flight
        )
        create_data["ticket"] = ticket

    # Створення об'єкта
    obj = model.objects.create(**create_data)

    # Побудова URL detail
    base_url = url_name.replace("-list", "")
    url = reverse(f"{base_url}-detail", args=[obj.pk])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    for field in info["serializer_fields"]:
        assert field in data
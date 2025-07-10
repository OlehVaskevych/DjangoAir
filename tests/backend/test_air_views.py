import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from air.models import AirlineUser, Flight, TicketStatusChoices

User = get_user_model()


@pytest.mark.django_db
def test_index_view(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200

    template_names = [t.name for t in response.templates if t.name is not None]
    assert any("home" in name for name in template_names)

    assert "flight_dates" in response.context
    assert "unique_cities" in response.context


@pytest.mark.django_db
def test_bookings_view_requires_auth(client):
    url = reverse("bookings")
    response = client.get(url)

    assert response.status_code in [302, 403]

    # Авторизуємо користувача
    user = User.objects.create_user(username="testuser", password="pass")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

    template_names = [t.name for t in response.templates if t.name is not None]
    assert any("bookings" in name for name in template_names)


@pytest.mark.django_db
def test_login_view_post_success(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="test@example.com", password="password123", username="testuser"
    )
    url = reverse("login")
    data = {"email": "test@example.com", "password": "password123"}
    response = client.post(url, data)
    json_response = response.json()
    print(json_response)
    assert response.status_code == 200
    assert json_response["success"] is True
    assert json_response["user"]["email"] == "test@example.com"


@pytest.mark.django_db
def test_login_view_post_invalid_password(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="test@example.com", password="password123", username="testuser"
    )
    url = reverse("login")
    data = {"email": "test@example.com", "password": "wrongpassword"}
    response = client.post(url, data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["success"] is False
    assert "general" in json_response["errors"]


@pytest.mark.django_db
def test_login_view_post_invalid_method(client):
    url = reverse("login")
    response = client.get(url)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["success"] is False
    assert "general" in json_response["errors"]


@pytest.mark.django_db
def test_register_view_post_success(client, django_user_model):
    url = reverse("register")
    data = {
        "first_name": "test",
        "last_name": "test",
        "email": "newuser@example.com",
        "password": "strongpass123",
        "confirm_password": "strongpass123",
        "agree_terms": True,
    }

    response = client.post(url, data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["success"] is True
    assert json_response["user"]["email"] == "newuser@example.com"
    assert User.objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_register_view_post_existing_email(client, django_user_model):
    existing_user = django_user_model.objects.create_user(
        email="exist@example.com", password="pass", username="testuser"
    )
    url = reverse("register")
    data = {
        "first_name": "test",
        "last_name": "test",
        "email": "exist@example.com",
        "password": "newpass123",
        "confirm_password": "newpass123",
        "agree_terms": True,
    }
    response = client.post(url, data)
    json_response = response.json()
    assert response.status_code == 400
    assert json_response["success"] is False
    assert "email" in json_response["errors"]


@pytest.mark.django_db
def test_register_view_post_invalid_method(client):
    url = reverse("register")
    response = client.get(url)
    json_response = response.json()
    assert response.status_code == 400
    assert json_response["success"] is False
    assert "error_message" in json_response


@pytest.mark.django_db
def test_logout_view_post(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="logout@example.com", password="pass", username="testuser_logout"
    )
    client.force_login(user)
    url = reverse("logout")
    response = client.post(url)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["success"] is True


@pytest.mark.django_db
def test_logout_view_invalid_method(client):
    url = reverse("logout")
    response = client.get(url)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["success"] is False


@pytest.mark.django_db
def test_create_checkout_session_post_success(mocker, client, django_user_model):
    user = django_user_model.objects.create_user(
        email="checkout@example.com", password="pass", username="user_checkout1"
    )
    client.force_login(user)
    url = reverse("create_checkout_session")

    # Підміна stripe.checkout.Session.create
    mock_session = mocker.Mock()
    mock_session.url = "http://mocked-session-url"
    mocker.patch("stripe.checkout.Session.create", return_value=mock_session)

    data = {
        "flightId": 1,
        "selectedSeats": [{"priceId": "price_1"}, {"priceId": "price_2"}],
        "selectedServices": {
            "meals": [{"priceId": "meal_price_1"}],
            "baggage": [{"priceId": "baggage_price_1"}],
            "comfort": [{"priceId": "comfort_price_1"}],
        },
    }
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    json_response = response.json()
    assert response.status_code == 200
    assert "url" in json_response
    assert json_response["url"] == "http://mocked-session-url"


@pytest.mark.django_db
def test_create_checkout_session_post_exception(mocker, client, django_user_model):
    user = django_user_model.objects.create_user(
        email="checkout2@example.com", password="pass", username="user_checkout2"
    )
    client.force_login(user)
    url = reverse("create_checkout_session")

    # Примусово викликаємо виключення
    def raise_exception(*args, **kwargs):
        raise Exception("Stripe error")

    mocker.patch("stripe.checkout.Session.create", side_effect=raise_exception)

    data = {"flightId": 1, "selectedSeats": [{"priceId": "price_1"}]}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    json_response = response.json()
    assert response.status_code == 500
    assert "error" in json_response


@pytest.mark.django_db
def test_create_checkout_session_invalid_method(client):
    url = reverse("create_checkout_session")
    response = client.get(url)
    json_response = response.json()
    assert response.status_code == 400
    assert "error" in json_response

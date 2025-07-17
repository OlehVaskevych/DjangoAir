from django.urls import include, path

from . import views

urlpatterns = [
    # Home page that contains form for select flight and seats
    path("", views.index, name="index"),
    path("bookings/", views.bookings, name="bookings"),

    path("staff_dashboard/gate_manager/", views.gate_manager, name="gate_manager"),
    path("staff_dashboard/checkin_manager/", views.checkin_manager, name="check_in_manager"),

    # Endpoint for creating a Stripe checkout session to process payments
    path(
        "create-checkout-session/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    # Endpoint for handling successful payment
    # Custom API endpoint to retrieve the tickets data assigned to current user
    # Authentication routes
    path("auth/login/", views.login, name="login"),
    path("auth/logout/", views.logout, name="logout"),
    path("auth/register/", views.register, name="register"),
    path("auth/services/", include("allauth.urls")),

    path("health/", views.health_check, name="health_check"),
]

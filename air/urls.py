from django.urls import path, include

from . import views

urlpatterns = [
    # Home page that contains form for select flight and seats
    path("", views.index, name="index"),

    path("bookings/", views.bookings, name="bookings"),

    # Endpoint for creating a Stripe checkout session to process payments
    path('create-checkout-session/', views.create_checkout_session, name="create_checkout_session"),

    # Endpoint for handling successful payment
    path('api/succeed_payment/', views.succeed_payment, name="succeed_payment"),
    # Custom API endpoint to retrieve the current authenticated user`s information
    path('api/current_user/', views.current_user, name="current_user"),
    # Custom API endpoint to retrieve the tickets data assigned to current user
    path('api/get_tickets/', views.get_tickets, name="get_tickets"),
    path('api/additional_services/', views.additional_services, name="additional_services"),
    path('api/cancel-ticket/', views.cancel_ticket, name="cancel_ticket"),

    # Authentication routes
    path('auth/login/', views.login, name="login"),
    path('auth/logout/', views.logout, name="logout"),
    path('auth/register/', views.register, name="register"),
    path('auth/services/', include('allauth.urls'))
]
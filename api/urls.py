from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdditionalServicesAPIView, AirlineUsersViewSet,
                    BaggageViewSet, BoardingPassViewSet, CancelTicketAPIView,
                    CheckInViewSet, ComfortViewSet, CurrentUserAPIView,
                    MealViewSet, StripeWebhookView, TicketViewSet,
                    UserTicketsAPIView, SeatMapAPIView, GetTicketsAPIView,
                    ConfirmBoardingAPIView, ConfirmCheckedInAPIView)

router = DefaultRouter()

router.register(r"users", AirlineUsersViewSet)
router.register(r"meals", MealViewSet)
router.register(r"baggages", BaggageViewSet)
router.register(r"comforts", ComfortViewSet)
router.register(r"tickets", TicketViewSet)
router.register(r"checkins", CheckInViewSet)
router.register(r"boardingpass", BoardingPassViewSet)

urlpatterns = [
    path(
        "additional_services/",
        AdditionalServicesAPIView.as_view(),
        name="additional_services",
    ),
    path("get_tickets/", UserTicketsAPIView.as_view(), name="get_tickets"),
    path("get_all_tickets/", GetTicketsAPIView.as_view(), name="get_upcoming_tickets"),
    path("cancel-ticket/", CancelTicketAPIView.as_view(), name="cancel_ticket"),
    path("succeed_payment/", StripeWebhookView.as_view(), name="succeed_payment"),

    path('flights/<int:flight_id>/seat-map/', SeatMapAPIView.as_view(), name="seat_map"),
    # Custom API endpoint to retrieve the current authenticated user`s information
    path("current_user/", CurrentUserAPIView.as_view(), name="current_user"),

    path("confirm-boardingpass/", ConfirmBoardingAPIView.as_view(), name="confirm_boardingpass"),
    path("confirm-checkedin/", ConfirmCheckedInAPIView.as_view(), name="confirm_checkedin"),
    path("", include(router.urls)),
]

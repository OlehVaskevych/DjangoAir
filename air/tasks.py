from celery import shared_task
from django.utils import timezone

from .models import Flight, FlightStatusChoices, Ticket, TicketStatusChoices


@shared_task
def update_flight_status():
    now = timezone.now()
    logger.info(f"[{now}] Task started")

    departed_flights = Flight.objects.filter(
        departure_time__lte=now,
        status=FlightStatusChoices.UPCOMING,
    )
    count_departed = departed_flights.update(status=FlightStatusChoices.IN_AIR)
    logger.info(f"Updated {count_departed} flights to 'IN_AIR'")

    arrived_flights = Flight.objects.filter(
        arrival_time__lte=now,
        status=FlightStatusChoices.IN_AIR,
    )
    count_arrived = arrived_flights.update(status=FlightStatusChoices.ARRIVED)
    logger.info(f"Updated {count_arrived} flights to 'ARRIVED'")

    updated_flight_ids = Flight.objects.filter(
        departure_time__lte=now,
        status=FlightStatusChoices.IN_AIR,
    ).values_list("id", flat=True)
    logger.debug(f"Flight IDs now IN_AIR: {list(updated_flight_ids)}")

    used_tickets = Ticket.objects.filter(
        flight_id__in=updated_flight_ids,
        status=TicketStatusChoices.UPCOMING,
        is_checked_in=True,
        is_boarded=True,
    )
    count_used_tickets = used_tickets.update(status=TicketStatusChoices.USED)
    logger.info(f"Updated {count_used_tickets} tickets to 'USED'")

    late_tickets = Ticket.objects.filter(
        flight_id__in=updated_flight_ids,
        status=TicketStatusChoices.UPCOMING,
    ).exclude(
        is_checked_in=True,
        is_boarded=True,
    )
    count_late_tickets = late_tickets.update(status=TicketStatusChoices.LATE)
    logger.info(f"Updated {count_late_tickets} tickets to 'LATE'")

    logger.info(f"[{timezone.now()}] Task finished")
    return "status"

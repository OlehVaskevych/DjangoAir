from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import BoardingPass, CheckIn, Ticket, TicketStatusChoices, AirlineUser, Flight, Seats
from .utils import generate_seats_for_flight, notify_user, get_users_for_flight, get_staff_for_airport


@receiver(pre_save, sender=AirlineUser)
def update_staff_and_superuser(sender, instance, **kwargs):
    if instance.role in [
        AirlineUser.Role.SUPERVISOR,
        AirlineUser.Role.GATE_MANAGER,
        AirlineUser.Role.CHECKIN_MANAGER,
    ]:
        instance.is_staff = True
        instance.is_superuser = instance.role == AirlineUser.Role.SUPERVISOR
    else:
        instance.is_staff = False
        instance.is_superuser = False


@receiver(post_save, sender=CheckIn)
def update_ticket_on_checkon(sender, instance, created, **kwargs):
    if created:
        ticket = instance.ticket
        ticket.is_checked = True
        ticket.status = TicketStatusChoices.CHECKED_IN
        ticket.save(update_fields=['is_checked_in', 'status'])

@receiver(post_save, sender=BoardingPass)
def update_ticket_on_boarding(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            ticket = instance.ticket
            ticket.is_boarded = True
            ticket.status = TicketStatusChoices.BOARDED
            ticket.save(update_fields=['is_boarded', 'status'])

@receiver(post_save, sender=Flight)
def auto_generate_seats(sender, instance, created, **kwargs):
    if created:
        generate_seats_for_flight(instance)

@receiver(post_save, sender=Ticket)
def reserve_seat_on_ticket_creation(sender, instance, created, **kwargs):
    if created:
        try:
            seat = Seats.objects.get(
                flight=instance.flight,
                seat_number=instance.seat_number,
            )
            if not seat.is_reserved:
                seat.is_reserved = True
                seat.save()
        except Seats.DoesNotExist:
            pass

@receiver(post_save, sender=Flight)
def flight_status_update(sender, instance, created, **kwargs):
    if not created and instance.tracker.has_changed('status'):
        old_status = instance.tracker.previous('status')
        new_status = instance.status

        origin = instance.origin
        origin_code = instance.origin_code
        destination = instance.destination
        destination_code = instance.destination_code

        user_message = None
        staff_message = None

        if old_status == 'upcoming':
            if new_status == 'in_air':
                user_message = f"Your flight {origin} [{origin_code}] → {destination} [{destination_code}] is now taking off."
                staff_message = f"Flight {origin_code} → {destination_code} has taken off. Check-in and boarding should be complete."
            elif new_status == 'canceled':
                user_message = f"Your flight {origin} [{origin_code}] → {destination} [{destination_code}] has been canceled."
                staff_message = f"Flight {origin_code} → {destination_code} has been canceled. Notify gate and check-in personnel."
            else:
                user_message = f"Your flight {origin} [{origin_code}] → {destination} [{destination_code}] changed status from «{old_status}» to «{new_status}»."
        else:
            user_message = f"Your flight {origin} [{origin_code}] → {destination} [{destination_code}] changed status from «{old_status}» to «{new_status}»."

        # Notify passengers
        if user_message:
            users_to_notify = get_users_for_flight(instance)
            for user in users_to_notify:
                notify_user(user.id, user_message)

        # Notify staff
        if staff_message:
            staff_users = get_staff_for_airport()
            for staff in staff_users:
                notify_user(staff.id, staff_message)


@receiver(post_save, sender=Ticket)
def ticket_gate_update(sender, instance, created, **kwargs):
    if not created:
        if instance.tracker.has_changed('gate'):
            old_gate = instance.tracker.previous('gate')
            new_gate = instance.gate

            message = (
                f"Gate for your ticket has been changed from GATE - {old_gate} to GATE - {new_gate}, "
                f"please download new ticket in 'my bookings' page!"
            )

            user_to_notify = instance.passenger.id
            notify_user(user_to_notify, message)
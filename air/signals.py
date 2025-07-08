from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import BoardingPass, CheckIn, Ticket, TicketStatusChoices, AirlineUser, Flight, Seats
from .utils import generate_seats_for_flight


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
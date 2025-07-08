from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BoardingPass, CheckIn, Ticket, TicketStatusChoices, AirlineUser


@receiver(pre_save, sender=AirlineUser)
def update_staff_and_superuser(sender, instance, **kwargs):
    if instance.role in [
        AirlineUser.Role.SUPERUSER,
        AirlineUser.Role.GATE_MANAGER,
        AirlineUser.Role.CHECKIN_MANAGER,
    ]:
        instance.is_staff = True
        instance.is_superuser = instance.role == AirlineUser.Role.SUPERUSER
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
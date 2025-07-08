from django.core.management.base import BaseCommand

from populate_db import populate


class Command(BaseCommand):
    help = "Populate database"

    def handle(self, *args, **kwargs):
        populate()
        self.stdout.write(self.style.SUCCESS("Successfully populated database!"))

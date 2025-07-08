from django.core.management.base import BaseCommand

from populate_db import clear


class Command(BaseCommand):
    help = "Clear all tables"

    def handle(self, *args, **kwargs):
        clear()
        self.stdout.write(self.style.SUCCESS("Successfully cleared all tables"))

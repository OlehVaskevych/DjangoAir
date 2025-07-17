import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_ENV", "DjangoAir.settings.dev"))
django.setup()

from DjangoAir.routing import application

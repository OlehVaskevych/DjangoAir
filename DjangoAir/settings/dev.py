from .base import *

DEBUG = True

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env('POSTGRES_DB_NAME'),
        "USER": env('POSTGRES_USER'),
        "PASSWORD": env('POSTGRES_PASSWORD'),
        "HOST": env('POSTGRES_HOST'),
        "PORT": env('POSTGRES_PORT'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
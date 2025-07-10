#!/bin/sh

echo "Gunicorn starts..."
exec gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8000 DjangoAir.wsgi:application

#!/bin/sh

echo "📦 Збираємо статику..."
python manage.py collectstatic --noinput

echo "🛠 Обробка міграцій..."
python manage.py migrate

python manage.py clear_db
python manage.py populate_db

echo "🚀 Запускаємо Gunicorn..."
gunicorn DjangoAir.wsgi:application --bind 0.0.0.0:8000

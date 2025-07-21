#!/bin/sh

echo "📦 Збираємо статику..."
python manage.py collectstatic --noinput

echo "🛠 Обробка міграцій..."
python manage.py migrate

echo "🚀 Запускаємо Daphne..."
daphne -b 0.0.0.0 -p 8000 DjangoAir.asgi:application


# =========================
# СТАДІЯ 1: Build Vue + Python deps
# =========================
FROM python:3.11-slim AS build

# Встановлюємо Node.js + системні пакети
RUN apt-get update && apt-get install -y \
    curl gnupg build-essential libpq-dev \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Робоча директорія
WORKDIR /app

# Python залежності
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Node залежності
COPY package*.json ./
RUN npm install

# Копіюємо увесь проєкт
COPY . .

# Збірка фронтенду (Vue, Webpack)
RUN npm run build

# Збірка статики Django
RUN python manage.py collectstatic --noinput

# =========================
# СТАДІЯ 2: Продакшн-образ
# =========================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Встановлюємо системні залежності (наприклад, для psycopg2)
RUN apt-get update && apt-get install -y libpq-dev

# Копіюємо Python-залежності та проєкт
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо лише готовий код з попереднього етапу
COPY --from=build /app /app

# Створюємо юзера
RUN adduser --disabled-password djangouser
RUN chown -R djangouser:djangouser /app
USER djangouser

# Встановлюємо змінні середовища
ENV DJANGO_SETTINGS_MODULE=DjangoAir.settings.prod

# Проброс порту
EXPOSE 8000

# Старт Gunicorn-сервера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "DjangoAir.wsgi:application"]

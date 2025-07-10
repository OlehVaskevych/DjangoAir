# =========================
# STAGE 1: Build Vue + Python deps
# =========================
FROM python:3.11-slim AS build

RUN apt-get update && apt-get install -y \
    curl gnupg build-essential libpq-dev \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# =========================
# STAGE 2: Prod
# =========================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build /app /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN adduser --disabled-password djangouser
RUN chown -R djangouser:djangouser /app
USER djangouser

ENV DJANGO_SETTINGS_MODULE=DjangoAir.settings.prod

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8000/health/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]

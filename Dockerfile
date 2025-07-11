# =============== СТАДІЯ 1: BUILD ===================
FROM python:3.11-slim AS build

# Системні пакети
RUN apt-get update && apt-get install -y \
    curl gnupg build-essential libpq-dev \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

WORKDIR /app

# Python залежності
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Node залежності
COPY package*.json ./
RUN npm install

# Копіюємо проєкт
COPY . .

# Збірка фронтенду (Vue)
RUN npm run build

# =============== СТАДІЯ 2: ПРОД ===================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

COPY --from=build /app /app

# Додаємо entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8000

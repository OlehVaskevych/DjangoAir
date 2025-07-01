FROM python:3.11

# Node.js для frontend (вбудовано)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update && apt-get install -y nodejs

# Робоча директорія
WORKDIR /app

# Python залежності
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Node.js залежності
COPY package.json package-lock.json ./
RUN npm install

# Копіюємо весь проєкт
COPY . .

# Збірка Vue/webpack (якщо є)
RUN npm run build

# Collect static якщо потрібно
# RUN python manage.py collectstatic --noinput

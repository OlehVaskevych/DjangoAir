# ✈️ DjangoAir

**DjangoAir** is a web service for buying airline tickets and managing the airport system. The project simulates the real work of an airport, dividing users into four main roles:

- 🧾 Passenger - can view flights and buy tickets online. Download his tickets or cancel.
- 🧾 Check-in manager - checks tickets and registers passengers.
- 🛂 Gate manager - manages passenger boarding.
- 🧑‍✈️ Supervisor - has access to administrative functionality.

---

## ⚙️ Main features

- Purchase of airline tickets with payment via Stripe
- Roles for staff with separate functionality
- Data storage in PostgreSQL
- Docker containers for full deployment

---

## 🚀 Quick start (via Docker)

### 1. Cloning the repository

```bash
git clone https://github.com/yourusername/DjangoAir.git
cd DjangoAir
```

### 2. Run
```bash
docker compose up --build
```

The service will be available on: http://localhost:8000

---

## 🛠 Running without Docker (optional)
If you want to run the project locally without Docker:

1. Install Redis, PostgreSQL and create an .env file

PostgreSQL docker run example:
```bash
docker run --name DjangoAir \
  -e POSTGRES_DB=DjangoAir \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres:latest
```

Redis docker run example:
```bash
docker run --name DjangoAir_redis \
  -p 6379:6379
  -d redis:latest
```

`.env` file must be in `DjangoAir/DjangoAir/.env` and must contains this options:
```.dotenv
DJANGO_SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
CLIENT_ID=
CLIENT_SECRET=
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
POSTGRES_DB_NAME=DjangoAir
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

2. Activate the virtual environment and install the dependencies

Run:
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
celery -A air worker --loglevel=info --pool=solo
celery -A air beat --loglevel=info
stripe listen --forward-to localhost:8000/api/succed_payment/
```
---

# Author
Oleh Vaskevych
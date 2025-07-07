# ✈️ DjangoAir

**DjangoAir** is a full-featured web service for purchasing airline tickets and managing airport operations. It simulates the real workflow of an airport, with four key user roles:

- 🧾 **Passenger** — View available flights, purchase tickets via Stripe, download or cancel tickets.
- 🧾 **Check-in Manager** — Validate tickets and register passengers.
- 🛂 **Gate Manager** — Manage the boarding process.
- 🧑‍✈️ **Supervisor** — Access administrative tools and dashboards.

---

## ⚙️ Features

- 💳 Secure ticket purchases via **Stripe**
- 👥 Role-based functionality for airport staff
- 🗄 PostgreSQL for persistent data storage
- 🐳 Dockerized deployment for easy setup
- ✉️ Email notifications for ticket purchases
- ⚙️ Background tasks handled by **Celery + Redis**

---

## 🚀 Quick Start (Docker)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/DjangoAir.git
cd DjangoAir
```

### 2. Launch the app
```bash
docker compose up --build
```

After that the service will be available at: https://localhost/

---

## 🛠 Manual Setup (Without Docker)

### 1. Requirements
Install and run the following manually:

- PostgreSQL
- Redis
- Python (recommended: 3.11)
- Stripe CLI (for local webhook testing)

PostgreSQL via Docker:
```bash
docker run --name djangoair-postgres \
  -e POSTGRES_DB=DjangoAir \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres:latest
```

Redis via Docker:
```bash
docker run --name djangoair-redis \
  -p 6379:6379 \
  -d redis:latest
```

### 2. Environment Variables
Create a .env file at: DjangoAir/DjangoAir/settings/.env

Here is example of .env file:
```dotenv
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True/False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web

STRIPE_SECRET_KEY=your_stripe_secret
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

CLIENT_ID=your_oauth_client_id
CLIENT_SECRET=your_oauth_client_secret

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

POSTGRES_DB_NAME=DjangoAir
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 3. Setup and Run

#### 1. Clone the repository and go into project folder.
```bash
git clone https://github.com/yourusername/DjangoAir.git
cd DjangoAir
```

#### 2. Create python venv and activate it.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install requirements.
```bash
pip install -r requirements.txt 
```

#### 4. Make migrations and collectstatic
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

In separate terminals, run:
```bash
# Celery worker
celery -A air worker --loglevel=info --pool=solo

# Celery beat (periodic tasks)
celery -A air beat --loglevel=info

# Stripe webhook listener
stripe listen --forward-to localhost:8000/api/succed_payment/
```

---

## 📂 Project Structure
```
DjangoAir/
├── air/                  # Main Django project
├── tickets/              # App for ticket management
├── users/                # User roles and auth
├── api/                  # REST API endpoints
├── static/               # Static files
├── templates/            # HTML templates
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Author
Oleh Vaskevych

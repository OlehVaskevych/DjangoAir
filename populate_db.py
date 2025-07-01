import random
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from air.models import *


def clear():
    AirlineUser.objects.all().delete()
    Meal.objects.all().delete()
    Baggage.objects.all().delete()
    Comfort.objects.all().delete()
    Airplane.objects.all().delete()
    Flight.objects.all().delete()
    Ticket.objects.all().delete()
    CheckIn.objects.all().delete()
    BoardingPass.objects.all().delete()

    print('All tables cleared successfully.')


def populate():

    fake = Faker()

    # Створюємо користувачів
    passengers = []
    for _ in range(10):
        user = AirlineUser.objects.create_user(
            username=fake.user_name(),
            password="testpassword123",
            email=fake.email(),
            role=AirlineUser.Role.PASSENGER,
        )
        passengers.append(user)

    # Створюємо літак
    airplane = Airplane.objects.create(name="Boeing 737", seat_capacity=150)

    flights = []
    for _ in range(3):
        departure = timezone.now() + timedelta(days=random.randint(1, 10))
        arrival = departure + timedelta(hours=random.randint(2, 8))

        flight = Flight.objects.create(
            flight_number=f"FL{random.randint(100, 999)}",
            origin=fake.city(),
            destination=fake.city(),
            origin_code=fake.country_code(),
            destination_code=fake.country_code(),
            departure_time=departure,
            arrival_time=arrival,
            base_price=random.uniform(100, 500),
            airplane=airplane,
        )
        flights.append(flight)

    dietary_options = [
        DietaryOption.objects.create(name="Low Calorie"),
        DietaryOption.objects.create(name="Vegetarian Option"),
        DietaryOption.objects.create(name="Dairy-Free Option"),
        DietaryOption.objects.create(name="Gluten-Free Option")
    ]

    meals = [Meal.objects.create(
        name='Vegetarian sandwich',
        description='Whole-grain baguette with bean lard, lettuce, pickle and parsley.',
        price=10,
        image_url='https://www.lot.com/content/dam/lot/marketing/sesja-zdjeciowa-posilkow-2023/posilki-prepaid/kanapka-wegetarianska-smalec.coreimg.82.760.jpg/1750838982457/kanapka-wegetarianska-smalec.jpg',
        stripe_price_id='price_1RP10YQMzydK9SUpLHKLiyJA'
    ), Meal.objects.create(
        name='Chicken salad',
        description='Salad with oriental spiced chicken with cucumber, cherry tomatoes, yellow bell pepper, sunflower seeds and tomato vinaigrette sauce.',
        price=15,
        image_url='https://www.lot.com/content/dam/lot/marketing/sesja-zdjeciowa-posilkow-2023/posilki-prepaid/salatka-kurczak-prepaid.coreimg.82.760.jpg/1696333346127/salatka-kurczak-prepaid.jpg',
        stripe_price_id='price_1RP4dAQMzydK9SUp98SUcXPx'
    ), Meal.objects.create(
        name='Breakfast',
        description='A breakfast set consisting of a wide selection of cold meats and cheeses with extras, a salmon roll and fruits.',
        price=34,
        image_url='https://www.lot.com/content/dam/lot/marketing/sesja-zdjeciowa-posilkow-2023/posilki-prepaid/posilek-sniadanie-prepaid.coreimg.82.760.jpg/1696333338749/posilek-sniadanie-prepaid.jpg',
        stripe_price_id='price_1RP4emQMzydK9SUpaNMtXCyj',
    ), Meal.objects.create(
        name='Chocolate cake',
        description='Chocolate cake with a bottle of sparkling Prosecco (200ml)',
        price=56,
        image_url='https://www.lot.com/content/dam/lot/marketing/sesja-zdjeciowa-posilkow-2023/posilki-prepaid/tort-czekoladowy-prosecco.coreimg.82.760.jpg/1697786794725/tort-czekoladowy-prosecco.jpg',
        stripe_price_id='price_1RP4h0QMzydK9SUpTkxR9mYz',
    )]

    meals[0].dietary_options.add(dietary_options[0], dietary_options[1])
    meals[1].dietary_options.add(dietary_options[2], dietary_options[3])
    meals[3].dietary_options.add(dietary_options[0])

    baggage_options = [
        Baggage.objects.create(
            name='Extra Carry-on',
            description='Additional cabin baggage up to 10kg',
            price=30,
            weight=10,
            stripe_price_id='',
        ),Baggage.objects.create(
            name='Additional Checked Bag',
            description='Extra checked luggage up to 23kg',
            price=50,
            weight=23,
            stripe_price_id='',
        ),Baggage.objects.create(
            name='Sports Equipment',
            description='Special handling for sports gear',
            price=40,
            weight=30,
            stripe_price_id='',
        ),Baggage.objects.create(
            name='Overweight Allowance',
            description='Increase weight limit for checked baggage',
            price=40,
            weight=10,
            stripe_price_id='',
        )
    ]

    comforts = [
        Comfort.objects.create(
            name='Priority Boarding',
            description='Be among the first to board the aircraft',
            price=15,
            stripe_price_id='price_1RP123QMzydK9SUpOHgHFvPz',
        ),Comfort.objects.create(
            name='Lounge Access',
            description='Enjoy exclusive airport lounge facilities',
            price=45,
            stripe_price_id='',
        ),Comfort.objects.create(
            name='In-flight Wi-Fi',
            description='Stay connected throughout your journey',
            price=12,
            stripe_price_id='',
        ),Comfort.objects.create(
            name='Travel Kit',
            description='Comfort kit with pillow, blanket and toiletries',
            price=20,
            stripe_price_id='',
        )
    ]

    # Створюємо квитки
    for user in passengers:
        flight = random.choice(flights)
        ticket = Ticket.objects.create(
            passenger=user,
            flight=flight,
            seat_number=f"{random.randint(1, 30)}{random.choice('ABCDEF')}",
            seat_class=random.choice(SeatClassChoices.values),
            price=flight.base_price + random.uniform(20, 100),
            booking_reference=generate_booking_reference()
        )
        ticket.meals.set(random.sample(meals, k=random.randint(0, 2)))
        ticket.baggage.set(random.sample(baggage_options, k=random.randint(0, 2)))
        ticket.comforts.set(random.sample(comforts, k=random.randint(0, 2)))

        # Чекін і посадковий талон випадково
        if random.choice([True, False]):
            CheckIn.objects.create(ticket=ticket, luggage_weight=random.uniform(5, 20))

        if random.choice([True, False]):
            BoardingPass.objects.create(
                ticket=ticket,
                gate_number=str(random.randint(1, 10)),
                boarding_time=timezone.now() + timedelta(minutes=random.randint(10, 60))
            )

    print("Database populated.")

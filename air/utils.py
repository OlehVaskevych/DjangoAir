import random
import string
import math

SEAT_CLASS_STRIPE_IDS = {
    "economy": "price_1RP0yYQMzydK9SUprJfIiJYw",
    "business": "price_1RP0yyQMzydK9SUpQVDc8Xlz",
    "first": "price_1RP0zFQMzydK9SUptZsV3qKC",
}

def find_best_seats_per_row(total_seats, max_columns):
    for i in range(min(total_seats, max_columns), 0, -1):
        if total_seats % i == 0:
            return i
    return 1

def get_stripe_price_id(seat_class):
    return SEAT_CLASS_STRIPE_IDS[seat_class]

def generate_unique_booking_reference(length=10, max_attempts=10):
    from .models import Ticket
    for _ in range(max_attempts):
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Ticket.objects.filter(booking_reference=ref).exists():
            return ref
    raise Exception('Could not generate unique booking reference')

# Generates a booking reference like 'A1B2C3D4E5'
def generate_booking_reference():
    """
    Generates a random 10-character booking reference consisting of
    uppercase letters and digits.

    Returns:
    - str: A 10-character alphanumeric booking reference.
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

def get_random_gate():
    return random.randint(2, 6)

def generate_seats_for_flight(flight):
    from .models import Seats, SeatClassChoices

    seat_config = [
        (SeatClassChoices.FIRST, flight.airplane.first_class_seats, 4),
        (SeatClassChoices.BUSINESS, flight.airplane.business_seats, 6),
        (SeatClassChoices.ECONOMY, flight.airplane.economy_seats, 6),
    ]

    current_row = 1

    for seat_class, total_seats, max_columns in seat_config:
        if total_seats == 0:
            continue

        seats_per_row = find_best_seats_per_row(total_seats, max_columns)
        rows_needed = total_seats // seats_per_row
        seat_letters = string.ascii_uppercase[:seats_per_row]

        seat_count = 0
        for _ in range(rows_needed):
            for letter in seat_letters:
                if seat_count >= total_seats:
                    break

                seat_number = f"{current_row}{letter}"
                Seats.objects.create(
                    flight=flight,
                    seat_number=seat_number,
                    seat_class=seat_class,
                    stripe_price_id=get_stripe_price_id(seat_class),
                    is_reserved=False,
                )
                seat_count += 1
            current_row += 1

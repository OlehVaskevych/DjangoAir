import random
import string
from .models import Ticket

def generate_unique_booking_reference(length=10, max_attempts=10):
    for _ in range(max_attempts):
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Ticket.objects.filter(booking_reference=ref).exists():
            return ref
    raise Exception('Could not generate unique booking reference')


def generate_booking_reference():
    # Генерація випадкового рядка з букв і цифр довжиною 10 символів
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

def get_random_gate():
    return random.randint(2, 6)

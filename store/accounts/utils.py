from random import randrange

from django.core.cache import cache


def generate_random_otp():
    return str(randrange(10000, 99999))


def verify_otp_code(code, phone_number):
    otp_code = cache.get(f'otp_{phone_number}')

    if otp_code is not None and otp_code == code:
        cache.delete(f'otp_{phone_number}')
        return True
    return False

import re
from django.contrib.auth.models import User


class Validate:

    @staticmethod
    def validate_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        error = ''

        if not re.fullmatch(regex, email):
            error = 'zadaný email není validní'
        if not User.objects.filter(email=email).exists():
            error = 'zadaný email není validní'

        return error


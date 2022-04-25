"""
Modul se třídou pro validaci emailů

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0


"""

import re
from django.contrib.auth.models import User


class Validate:
    """třída s jednou funkcí na validaci emailů pomocí regu"""
    @staticmethod
    def validate_email(email):
        """funkce validiuje emaily v podobe Stringu
        @param email: text emailu ...(nekdo@neco.com)

        @return seznam chyb or None
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        error = ''

        if not re.fullmatch(regex, email):
            error = 'zadaný email není validní'
        if not User.objects.filter(email=email).exists():
            error = 'zadaný email není validní'

        return error


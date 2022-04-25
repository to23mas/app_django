"""
modul umožňující odesílání emailů

@author: Tomáš Míčka

classes: Mailer

@contact: to23mas@gmail.com

@version:  1.0
"""


from django.core.mail import send_mail
from app import settings



class Mailer:
    """Třída zařizující práci s emailem a poštou"""


    def __init__(self, subject, addressee, message):
        """ funkce vytváří základní podobu s emailu

        @param subject: předmět emailu
        @param addressee: adresát (nekdo@email.com)
        @param message: zpráva
        """
        self.subject = subject
        self.addressee = addressee
        self.message = message



    def send_mail(self):
        """funkce odesílá připravený email a vrací True, pokud se podařilo odeslat"""
        mail = send_mail(self.subject,
                         self.message,
                         settings.EMAIL_HOST_USER,
                         [self.addressee])
        if mail == 1:
            return True
        else:
            return False

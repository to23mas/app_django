from django.core.mail import send_mail
from app import settings
from django.core.validators import validate_email


class Mailer:
    def __init__(self, subject, addressee, message):
        self.subject = subject
        self.addressee = addressee
        self.message = message



    def send_reset_password(self):
        """this function send email and return true if it is succecsfull"""
        mail = send_mail(self.subject,
                         self.message,
                         settings.EMAIL_HOST_USER,
                         [self.addressee])
        if mail == 1:
            return True
        else:
            return False

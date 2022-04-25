"""
modul pro práci s formulářem

formuláře pro registraci uživatelů


classes: CustomUserForm

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomUserForm(UserCreationForm):
    """Třída pro formulář registrace rozšiřuje UserCreationForm.

    @param hpassword1: představuje pole s heslem a nápovědou
    @param hpassword: pole pro ověření hesla s nápovědou

    V META tříde je vybráno
    model: User class
    fields: ['username', 'email', 'password1', 'password2']
    labels, změna popisů pro pole s přezdívkou a emailem
    """


    password1 = forms.CharField(
        label='Heslo',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_('''Heslo je příliš npodobné ostatním osobním informacím.
Heslo musí obsahovat alespoň 8 znaků.
Heslo nesmí mít běžnou podobu ...(123456).
Heslo musí obsahovat alespoň jedno písmeno.'''),
    )
    password2 = forms.CharField(
        label='Heslo znouvu',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_('Vlož stejné heslo jako předtím.'),
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        labels = {
            'username': ('Přezdívka'),
            'email': ('Email')
        }


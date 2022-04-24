from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext, gettext_lazy as _

class CustomUserForm(UserCreationForm):


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


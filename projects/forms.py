# import form class from django
from django import forms
from .models import Ukol, UserAccount


# create a ModelForm
class UkolForm(forms.ModelForm):
    class Meta:
        model = Ukol
        fields = "__all__"
        exclude = ['user']


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = "__all__"
        exclude = ['user']
        widgets = {
            'heslo': forms.PasswordInput(),
            'heslo_znovu': forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = "__all__"
        exclude = ['user', 'heslo_znovu', 'email']
        widgets = {
            'heslo': forms.PasswordInput(),
        }

"""
modul pro práci s formulářem

formuláře pro přidávání úkolů, pro přidávání účtů a pro přihlašování v testovacích projektech


classes: UkolForm, RegisterForm, LoginForm

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""


from django import forms
from .models import Ukol, UserAccount



class UkolForm(forms.ModelForm):
    """Třída pro formulář, který přidává úkolu do úkolníčku.

        V META tříde je vybráno
        model: Ukol class
        fields: všechny pole z modelu
        exclude: pole s názvem user nebude ve formuláři
        """

    class Meta:
        model = Ukol
        fields = "__all__"
        exclude = ['user']


class RegisterForm(forms.ModelForm):
    """Třída pro formulář, který registuje účty

        V META tříde je vybráno
        model: User accounts class
        fields: všechny pole z modelu
        exclude: pole s názvem user nebude ve formuláři
        widgets: widgety pro hesla
        """
    class Meta:
        model = UserAccount
        fields = "__all__"
        exclude = ['user']
        widgets = {
            'heslo': forms.PasswordInput(),
            'heslo_znovu': forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):
    """Třída pro formulář, který přihlašuje vytvořené účty

            V META tříde je vybráno
            model: User accounts class
            fields: všechny pole z modelu
            exclude: pole s názvem user nebude ve formuláři
            widgets: widgety pro heslo
            """
    class Meta:
        model = UserAccount
        fields = "__all__"
        exclude = ['user', 'heslo_znovu', 'email']
        widgets = {
            'heslo': forms.PasswordInput(),
        }

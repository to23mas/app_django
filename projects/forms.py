# import form class from django
from django import forms
from .models import Ukol


# create a ModelForm
class UkolForm(forms.ModelForm):


    # specify the name of model to use
    class Meta:
        model = Ukol
        fields = "__all__"
        exclude = ['user']

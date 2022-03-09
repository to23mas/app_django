from django import forms

class SingelForm(forms.Form, data):

    ansvers = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())


class MultiForm(forms.Form):
    pass

class OpenForm(forms.Form):
    pass

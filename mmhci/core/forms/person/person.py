# forms.py
from django import forms


class PersonForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    preferred_name = forms.CharField()
    dob = forms.DateField()
    phone = forms.CharField()
    email = forms.EmailField()

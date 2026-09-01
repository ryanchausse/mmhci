# forms.py
from django import forms


class PersonForm(forms.Form):
    # Forms are for custom display and validation of/on user-facing inputs
    first_name = forms.CharField()
    last_name = forms.CharField(
        required=False,
    )
    preferred_name = forms.CharField(
        required=False,
    )
    dob = forms.DateField(
        label='Date of birth',
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'placeholder': '0411 222 333'
            }
        )
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'sample@email.com'
            }
        )
    )

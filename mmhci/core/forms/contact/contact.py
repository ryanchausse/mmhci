from django import forms

from mmhci.core.models.person.person import Person


class ContactForm(forms.Form):
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        empty_label="Select Person",
        required=True
    )
    type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
            }
        ),
        required=False
    )
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
            }
        ),
        required=False
    )

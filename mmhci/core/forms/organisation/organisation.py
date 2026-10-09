from django import forms


class OrganisationForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )

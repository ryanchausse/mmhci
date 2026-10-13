from django import forms


class UserForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'sample@email.com'
            }
        )
    )

from django import forms

from mmhci.core.models.organisation.organisation import Organisation
from mmhci.core.models.organisation.organisation_role import OrganisationRole


class OrganisationGroupForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
            }
        )
    )
    organisation = forms.ModelChoiceField(
        queryset=Organisation.objects.all(),
        empty_label="Select Organisation",
        required=True
    )
    organisation_roles = forms.ModelMultipleChoiceField(
        # TODO: filter by permissions
        queryset=OrganisationRole.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Org Role(s)"
    )

from django import forms
from django.contrib.auth import get_user_model

from mmhci.core.models.organisation.organisation_group import OrganisationGroup


# TODO: filter by permissions
class OrganisationGroupMembershipForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        empty_label="Select User",
        required=True
    )
    organisation_group = forms.ModelChoiceField(
        queryset=OrganisationGroup.objects.all(),
        empty_label="Select Org Group",
        required=True
    )
    description = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )

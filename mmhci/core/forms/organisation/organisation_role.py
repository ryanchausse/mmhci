from django import forms
from django.contrib.auth.models import Permission
from django.db.models import Q

from mmhci.core.orchestrations.config.default_admin_permissions import default_admin_role_permissions
from mmhci.core.models.organisation.organisation import Organisation


class OrganisationRoleForm(forms.Form):
    filtered_permissions = None
    # TODO: move into view or service layer to fine-grain permission assignment.
    # Can perhaps only delegate one's own permissions. For now, it will be
    # assumed that only org admins have the power to assign permissions
    permissions_query = Q()
    for app_model_str, excluded_codenames in default_admin_role_permissions.items():
        app_label, model_name = app_model_str.split('.')
        model_q = Q(
            content_type__app_label=app_label,
            content_type__model=model_name
        )
        if excluded_codenames:
            model_q &= ~Q(codename__in=excluded_codenames)
        permissions_query |= model_q
    filtered_permissions = Permission.objects.filter(permissions_query)

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
            }
        ),
        required=True
    )
    description = forms.CharField(required=False)
    # TODO: filter by user admin permissions
    organisation = forms.ModelChoiceField(
        queryset=Organisation.objects.all(),
        empty_label="Select Organisation",
        required=True
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=filtered_permissions,
        widget=forms.CheckboxSelectMultiple,
        label="Select Permissions for Role"
    )

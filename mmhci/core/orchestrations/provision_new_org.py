# Creates new org, including admin role and admins group
# A superuser can then give a user a membership to the admin org group
# If a "CreateOrganisation" service exists, might need to replace in
# views and API with this orchestration

from django.db import transaction
from django.contrib.auth.models import Permission
from mmhci.core.models.organisation import Organisation
from mmhci.core.models.organisation import OrganisationGroup
from mmhci.core.models.organisation import OrganisationRole
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService
from mmhci.core.orchestrations.config.default_admin_permissions import default_admin_role_permissions


class ProvisionNewOrg(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    # Business rule validation lives in single-domain (model) services.
    # Multiple model/multi-stage orchestrations can import multiple
    # single-domain services.
    required_permissions = frozenset({'core.can_provision_new_org'})

    def __init__(self, request, org_name):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.org_name = org_name

    @transaction.atomic
    def execute(self):
        with self.audit_write():
            # TODO: change these to use individual model services
            organisation = Organisation.objects.get_or_create(
                name=self.org_name
            )
            organisation_role = OrganisationRole.objects.get_or_create(
                organisation=organisation,
                permissions=None,
                name="Admin"
            )
            organisation_group = OrganisationGroup.objects.get_or_create(
                organisation=organisation,
                roles=None,
                name="Admins"
            )
            organisation_group.roles.add(organisation_role)

        # Add admin role permissions
        for model_str, exclude_list in default_admin_role_permissions.items():
            app_label, model_name = model_str.lower().split(".")
            exclude_list = exclude_list or []

            perms = Permission.objects.filter(
                content_type__app_label=app_label,
                content_type__model=model_name
            )

            if exclude_list:
                perms = perms.exclude(codename__in=exclude_list)

            with self.audit_write():
                organisation_role.permissions.add(*perms)

        return organisation

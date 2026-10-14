from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.organisation import OrganisationRole
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class UpdateOrganisationRoleService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.change_organisationrole'})

    def __init__(self, request, pk=None, data=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.data = data

    @transaction.atomic
    def execute(self):
        if self.pk:
            organisation_role = get_object_or_404(OrganisationRole, pk=self.pk)
        organisation_role.name = self.data["name"]
        organisation_role.description = self.data["description"]
        organisation_role.organisation = self.data["organisation"]
        with self.audit_write():
            organisation_role.save()
            organisation_role.permissions.set(self.data["permissions"])

        return organisation_role

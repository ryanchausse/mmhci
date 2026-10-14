from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.organisation import OrganisationGroup
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class UpdateOrganisationGroupService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.change_organisationgroup'})

    def __init__(self, request, pk=None, data=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.data = data

    @transaction.atomic
    def execute(self):
        if self.pk:
            organisation_group = get_object_or_404(OrganisationGroup, pk=self.pk)
        organisation_group.name = self.data["name"]
        organisation_group.organisation = self.data["organisation"]
        with self.audit_write():
            organisation_group.save()
            organisation_group.roles.set(self.data["organisation_roles"])

        return organisation_group

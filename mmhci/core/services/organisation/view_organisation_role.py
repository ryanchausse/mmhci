from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.organisation import OrganisationRole
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class ViewOrganisationRoleService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.view_organisationrole'})

    def __init__(self, request, pk=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk

    @transaction.atomic
    def execute(self):
        if self.pk:
            organisation_role = get_object_or_404(OrganisationRole, pk=self.pk)
        self.log_access(organisation_role)
        return organisation_role

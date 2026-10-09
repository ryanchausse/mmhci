from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.organisation import Organisation
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class ViewOrganisationService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.view_organisation'})

    def __init__(self, request, pk=None, uuid=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.uuid = uuid

    @transaction.atomic
    def execute(self):
        if self.pk:
            organisation = get_object_or_404(Organisation, pk=self.pk)
        elif self.uuid:
            organisation = get_object_or_404(Organisation.objects.filter(uuid=self.uuid))
        self.log_access(organisation)
        return organisation

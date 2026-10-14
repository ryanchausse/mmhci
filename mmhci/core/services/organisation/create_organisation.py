from django.db import transaction
from mmhci.core.models.organisation import Organisation
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class CreateOrganisationService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    # Business rule validation lives in single-domain (model) services.
    # Multiple model/multi-stage orchestrations can import multiple
    # single-domain services.
    required_permissions = frozenset({'core.create_organisation'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        with self.audit_write():
            # TODO: Gate by permissions.
            organisation, _ = Organisation.objects.get_or_create(
                name=self.data["name"],
                description=self.data["description"]
            )

        return organisation

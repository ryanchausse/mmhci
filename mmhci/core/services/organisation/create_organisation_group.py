from django.db import transaction
from mmhci.core.models.organisation import OrganisationGroup
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class CreateOrganisationGroupService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.create_organisationgroup'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        with self.audit_write():
            # TODO: Gate by permissions.
            organisation_group = OrganisationGroup.objects.create(
                name=self.data["name"],
                organisation=self.data["organisation"]
                # roles=None  # Need to create the group before M:M assignment
            )
            organisation_group.roles.set(self.data["organisation_roles"])
        return organisation_group

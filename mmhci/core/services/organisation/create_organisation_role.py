from django.db import transaction
from mmhci.core.models.organisation import OrganisationRole
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService

class CreateOrganisationRoleService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.create_organisationrole'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        with self.audit_write():
            # TODO: Gate by permissions.
            organisation_role = OrganisationRole.objects.create(
                name=self.data["name"],
                description=self.data["description"],
                organisation=self.data["organisation"]
                # permissions=None  # Need to create the role before M:M assignment
            )
            organisation_role.permissions.set(self.data["permissions"])
        return organisation_role

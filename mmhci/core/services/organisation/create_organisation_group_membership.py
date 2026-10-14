from django.db import transaction
from mmhci.core.models.organisation import OrganisationGroupMembership
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class CreateOrganisationGroupMembershipService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.create_organisationgroupmembership'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        with self.audit_write():
            # TODO: Gate by permissions.
            organisation_group_membership = OrganisationGroupMembership.objects.create(
                user=self.data["user"],
                organisation_group=self.data["organisation_group"],
                description=self.data["description"]
            )
        return organisation_group_membership

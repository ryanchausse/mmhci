from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.organisation import OrganisationGroupMembership
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class UpdateOrganisationGroupMembershipService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.change_organisationgroupmembership'})

    def __init__(self, request, pk=None, data=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.data = data

    @transaction.atomic
    def execute(self):
        if self.pk:
            organisation_group_membership = get_object_or_404(OrganisationGroupMembership, pk=self.pk)
        organisation_group_membership.user = self.data["user"]
        organisation_group_membership.organisation_group = self.data["organisation_group"]
        organisation_group_membership.description = self.data["description"]
        with self.audit_write():
            organisation_group_membership.save()

        return organisation_group_membership

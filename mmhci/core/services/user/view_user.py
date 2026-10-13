from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.users.models import User
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class ViewUserService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'users.view_user'})

    def __init__(self, request, pk=None, uuid=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.uuid = uuid

    @transaction.atomic
    def execute(self):
        if self.pk:
            user = get_object_or_404(User, pk=self.pk)
        elif self.uuid:
            user = get_object_or_404(User.objects.filter(uuid=self.uuid))
        if user.owning_organisation_id not in self.authorized_org_ids:
            raise PermissionDenied("You do not have permission for this User.")
        self.log_access(user)
        return user

from django.core.exceptions import PermissionDenied

from mmhci.users.models import User
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class ListUsersService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'users.can_view_user_list'})

    def __init__(self, request):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request

    def execute(self):
        if not self.authorized_org_ids:
            raise PermissionDenied(
                "You do not have permission to see a list of Users."
            )
        users = User.objects.all()
        return users

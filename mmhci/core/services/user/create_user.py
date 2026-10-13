from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import transaction
from mmhci.core.models.organisation import Organisation

from mmhci.core.forms.user.user import UserForm
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService

class CreateUserService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'users.add_user'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        # Does this user have permission to add a User in their
        # current org? Current org id is set in middleware
        current_org = Organisation.objects.get(
            pk=self.request.session.get("current_org_id")
        )
        if not self.request.session.get("current_org_id") in self.authorized_org_ids:
            raise PermissionError("You cannot create a User in the current org.")

        with self.audit_write():
            # User creation has a custom save_model() in the Admin interface
            User = get_user_model()
            user = User(
                email=self.data["email"],
                owning_organisation=current_org
            )
            user_form = UserForm(initial={"email": self.data["email"]})
            user_admin_instance = admin.site._registry[User]
            user_admin_instance.save_model(
                request=self.request, 
                obj=user, 
                form=user_form, 
                change=False
            )

        return user

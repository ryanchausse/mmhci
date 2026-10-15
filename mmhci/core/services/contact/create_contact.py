from django.db import transaction
from mmhci.core.models.organisation import Organisation
from mmhci.core.models.contact import Contact
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class CreateContactService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.add_contact'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        current_org = Organisation.objects.get(
            pk=self.request.session.get("current_org_id")
        )
        if not self.request.session.get("current_org_id") in self.authorized_org_ids:
            raise PermissionError(
                "You cannot create a Contact in the current organisation."
            )

        with self.audit_write():
            contact = Contact.objects.create(
                person=self.data["person"],
                type=self.data["type"],
                description=self.data["description"],
                owning_organisation=current_org
            )

        return contact

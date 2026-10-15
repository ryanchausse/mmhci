from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.contact import Contact
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class UpdateContactService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.change_contact'})

    def __init__(self, request, pk=None, uuid=None, data=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.uuid = uuid
        self.data = data

    @transaction.atomic
    def execute(self):
        if self.pk:
            contact = get_object_or_404(Contact, pk=self.pk)
        elif self.uuid:
            contact = get_object_or_404(Contact.objects.filter(uuid=self.uuid))
        if contact.owning_organisation_id not in self.authorized_org_ids:
            raise PermissionDenied(
                "You do not have permission to update this Contact."
            )
        contact.person = self.data["person"]
        contact.type = self.data["type"]
        contact.description = self.data["description"]
        # NB: updating the owning organisation might need a new form field
        # and/or a new orchestration or service
        # contact.owning_organisation = self.data["owning_organisation"]
        with self.audit_write():
            contact.save()

        return contact

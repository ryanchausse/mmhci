from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.contact import Contact
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class ViewContactService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.view_contact'})

    def __init__(self, request, pk=None, uuid=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.uuid = uuid

    @transaction.atomic
    def execute(self):
        if self.pk:
            contact = get_object_or_404(Contact, pk=self.pk)
        elif self.uuid:
            contact = get_object_or_404(Contact.objects.filter(uuid=self.uuid))
        if contact.owning_organisation_id not in self.authorized_org_ids:
            raise PermissionDenied(
                "You do not have permission to view this Contact."
            )
        self.log_access(contact)
        return contact

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.person import Person
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class ViewPersonService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.view_person'})

    def __init__(self, request, pk=None, uuid=None):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.uuid = uuid

    @transaction.atomic
    def execute(self):
        if self.pk:
            person = get_object_or_404(Person, pk=self.pk)
        elif self.uuid:
            person = get_object_or_404(Person.objects.filter(uuid=self.uuid))
        if person.owning_organisation_id not in self.authorized_org_ids:
            raise PermissionDenied("You do not have permission for this Person.")
        self.log_access(person)
        return person

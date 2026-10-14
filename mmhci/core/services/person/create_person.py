from django.db import transaction
from mmhci.core.models.organisation import Organisation
from mmhci.core.models.person import Person
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


class CreatePersonService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    # Business rule validation lives in single-domain (model) services.
    # Multiple model/multi-stage orchestrations can import multiple
    # single-domain services.
    required_permissions = frozenset({'core.add_person'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        # Does this user have permission to add a Person in their
        # current org? Current org id should be set in middleware
        current_org = Organisation.objects.get(
            pk=self.request.session.get("current_org_id")
        )
        if not self.request.session.get("current_org_id") in self.authorized_org_ids:
            raise PermissionError("You cannot create a Person in the current org.")

        with self.audit_write():
            person = Person.objects.create(
                first_name=self.data["first_name"],
                last_name=self.data["last_name"],
                preferred_name=self.data["preferred_name"],
                dob=self.data["dob"],
                phone=self.data["phone"],
                email=self.data["email"],
                owning_organisation=current_org
            )

        return person

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.person import Person
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


# This needs to change. This service layer should have no knowledge of the form
# object. Need to unpack variables and send to this layer instead of sending
# the whole form object. This will make the service re-usable by e.g. the API
# layer, and also more testable. The correct usage is like:
# From view layer, instantiate service with a call passing no vars:
# view_person_service = ViewOrUpdatePersonService()
# Then,
# view_person_result = view_person_service.execute(**form.cleaned_data)
# Then, this service's execute() method can extract all necessary dict data.
# execute(self, first_name: str, last_name: str, etc.) -> Person
# If there are a lot of values, I could maybe use a Pydantic class to parse the
# incoming data instead of manually maintaining a big argument list here. Make
# similar changes to the new CreatePersonService.
# The __init__() method in these services should be used mainly for
# infrastructure items like dependency injection.
class ViewOrUpdatePersonService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    required_permissions = frozenset({'core.view_person'})

    def __init__(self, request, pk=None, form=None, update=False):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.pk = pk
        self.form = form
        self.update = update

    @transaction.atomic
    def execute(self):
        person = get_object_or_404(
            Person,
            pk=self.pk
        )
        if person.owning_organisation_id not in self.authorized_org_ids:
            raise PermissionDenied("You do not have permission to access this Person.")
        if not self.form or not self.update:
            self.log_access(person)
            return person
        person.first_name=self.form.cleaned_data["first_name"]
        person.last_name=self.form.cleaned_data["last_name"]
        person.preferred_name=self.form.cleaned_data["preferred_name"]
        person.dob=self.form.cleaned_data["dob"]
        person.phone=self.form.cleaned_data["phone"]
        person.email=self.form.cleaned_data["email"]
        with self.audit_write():
            person.save()

        return person

from django.db import transaction
from django.shortcuts import get_object_or_404

from mmhci.core.models.person import Person


class ViewOrUpdatePersonService:
    def __init__(self, request, pk=None, form=None, update=False):
        self.request = request
        self.pk = pk
        self.form = form
        self.update = update

    @transaction.atomic
    def execute(self):
        # TODO: enforce permissions (set permission name as a string)
        # Possibly need to place permission logic here instead of in the Views/API
        # routers so permissions are enforced no matter where the call comes from.
        # Maybe create a service base class that does this? In the current plan, we
        # would need the user and the org_id (org context)
        person = get_object_or_404(Person, pk=self.pk)
        if not self.form or not self.update:
            return person
        person.first_name=self.form.cleaned_data["first_name"]
        person.last_name=self.form.cleaned_data["last_name"]
        person.preferred_name=self.form.cleaned_data["preferred_name"]
        person.dob=self.form.cleaned_data["dob"]
        person.phone=self.form.cleaned_data["phone"]
        person.email=self.form.cleaned_data["email"]
        person.save()

        return person

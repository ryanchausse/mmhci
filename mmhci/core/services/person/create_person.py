from django.db import transaction
from mmhci.core.models.person import Person

class CreatePersonService:
    # Business rule validation lives in single-domain (model) services. Multiple model/
    # multi-stage orchestrations can import multiple single-domain services.

    # NB: need to save fields manually because PersonForm inherits from forms.Form,
    # not forms.ModelForm
    def __init__(
        self,
        first_name,
        last_name,
        preferred_name,
        dob,
        phone,
        email
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_name = preferred_name
        self.dob = dob
        self.phone = phone
        self.email = email

    @transaction.atomic
    def execute(self):
        person = Person.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            preferred_name=self.preferred_name,
            dob=self.dob,
            phone=self.phone,
            email=self.email
        )
        return person

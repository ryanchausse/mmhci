"""
Model
  - Person

Possibly needs a relational table to Organisation to represent "assigned org"
"""
import uuid
from django.db import models

from auditlog.registry import auditlog
from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase

AUDIT_EXCLUSIONS = [
    "last_name",
    "email"
]

@auditlog.register(exclude_fields=AUDIT_EXCLUSIONS)
class Person(CreatedAndUpdatedBase):
    # Models enforce validation of data integrity-related invariants
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    address = models.ForeignKey(
        "core.Address", on_delete=models.PROTECT, null=True, blank=True
    )
    first_name = models.TextField()
    middle_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(blank=True)
    preferred_name = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    # Consider using pip package django-phonenumber-field. For now, be permissive.
    phone = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    def get_full_name_dict(self):
        first_name = None
        preferred_name = None
        middle_name = None
        last_name = None
        # Be safe, even if first_name is required
        if self.first_name:
            first_name = self.first_name
        if self.preferred_name:
            preferred_name = self.preferred_name
        if self.middle_name:
            middle_name = self.middle_name
        if self.last_name:
            last_name = self.last_name
        return {
            "first_name": first_name,
            "preferred_name": preferred_name,
            "middle_name": middle_name,
            "last_name": last_name
        }

    def get_full_name_string(self, include_preferred=True):
        full_name_string = ""
        full_name_dict = self.get_full_name_dict()
        for name_type, name_value in full_name_dict.items():
            if name_value:
                if name_type != "preferred_name":
                    full_name_string += name_value
                elif include_preferred:
                    full_name_string += "'" + name_value + "'"
                full_name_string += " "
        # TODO: reduce stupidity
        return full_name_string.strip()

    def get_full_name_string_private(self, include_preferred=True):
        full_name_string_private = ""
        full_name_dict = self.get_full_name_dict()
        for name_type, name_value in full_name_dict.items():
            if name_value:
                if name_type != "preferred_name":
                    full_name_string_private += name_value[0]
                elif include_preferred:
                    full_name_string_private += "'" + name_value[0] + "'"
                full_name_string_private += " "
        # TODO: reduce stupidity
        return full_name_string_private.strip()

    @property
    def full_name(self):
        return self.get_full_name_string()

    @property
    def full_legal_name(self):
        return self.get_full_name_string_private(include_preferred=False)

    @property
    def full_name_private(self):
        return self.get_full_name_string_private()

    @property
    def full_legal_name_private(self):
        return self.get_full_name_string_private(include_preferred=False)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return (
            f"{self.uuid} - {self.full_name_private}"
        )

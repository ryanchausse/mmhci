"""
Model
  - Person
"""

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
    address = models.ForeignKey(
        "core.Address", on_delete=models.PROTECT, null=True, blank=True
    )
    # If last_name, or first_name/last_name/etc. become constrained as unique,
    # perhaps we can introduce null=True in these TextField()s
    first_name = models.TextField()
    last_name = models.TextField(blank=True)
    preferred_name = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    # Consider using pip package django-phonenumber-field. For now, permissive.
    phone = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return (
            f"Person Name: {self.first_name} '{self.preferred_name}' {self.last_name}"
        )

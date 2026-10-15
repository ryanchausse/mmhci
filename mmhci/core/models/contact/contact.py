"""
Model
  - Contact (a call/email/etc., possibly incoming? Maybe incoming is a separate model?)
"""
import uuid
from django.db import models

from auditlog.registry import auditlog
from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase

AUDIT_EXCLUSIONS = [
    "description"
]


@auditlog.register(exclude_fields=AUDIT_EXCLUSIONS)
class Contact(CreatedAndUpdatedBase):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    description = models.TextField(null=True, blank=True)
    person = models.ForeignKey(
        "core.Person", on_delete=models.PROTECT, null=True, blank=True
    )
    type = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.type} - {self.person}"

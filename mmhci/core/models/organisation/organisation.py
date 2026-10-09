"""
Model
  - Organisation

"""
import uuid
from django.db import models

from auditlog.registry import auditlog
from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase

AUDIT_EXCLUSIONS = []


@auditlog.register(exclude_fields=AUDIT_EXCLUSIONS)
class Organisation(CreatedAndUpdatedBase):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.TextField()
    description = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["name"]
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self):
        return f"Organisation Name: {self.name}"

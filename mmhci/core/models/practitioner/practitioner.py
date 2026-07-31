"""
Model
  - Practitioner
"""

from django.conf import settings
from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Practitioner(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField()
    # Practitioner possibly has a user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )
    phone = models.TextField()

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Practitioner"
        verbose_name_plural = "Practitioners"

    def __str__(self):
        return f"Practitioner Name: {self.name}"

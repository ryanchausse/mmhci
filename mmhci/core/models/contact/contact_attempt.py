"""
Model
  - ContactAttempt (outgoing - an attempt to contact a Person)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ContactAttempt(CreatedAndUpdatedBase):
    contact = models.ForeignKey(
        "core.Contact", on_delete=models.PROTECT, null=True, blank=True
    )
    description = models.TextField()
    method = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactAttempt"
        verbose_name_plural = "ContactAttempts"

    def __str__(self):
        return f"ContactAttempt Contact: {self.contact}, Method: {self.method}"

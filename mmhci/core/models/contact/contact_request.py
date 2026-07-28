"""
Model
  - ContactRequest (formerly "CallbackRequest")
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class ContactRequest(CreatedAndUpdatedMetaModel):
    contact = models.ForeignKey(
        "core.Contact", on_delete=models.PROTECT, null=True, blank=True
    )
    description = models.TextField()
    method = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactRequest"
        verbose_name_plural = "ContactRequests"

    def __str__(self):
        return f"ContactRequest Contact: {self.contact}, Method: {self.method}"

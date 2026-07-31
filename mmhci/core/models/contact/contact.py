"""
Model
  - Contact (a call/email/etc., possibly incoming? Maybe incoming is a separate model?)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Contact(CreatedAndUpdatedBase):
    description = models.TextField()
    person = models.ForeignKey(
        "core.Person", on_delete=models.PROTECT, null=True, blank=True
    )
    type = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"Contact Type: {self.type}, Person: {self.person}"

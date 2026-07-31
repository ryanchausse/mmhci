"""
Model
  - ContactNote (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ContactNote(CreatedAndUpdatedBase):
    name = models.TextField()
    contact = models.ForeignKey("core.Contact", on_delete=models.PROTECT)
    description = models.TextField()
    note = models.ForeignKey("core.Note", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactNote"
        verbose_name_plural = "ContactNotes"

    def __str__(self):
        return f"Contact: {self.contact}, Note: {self.note}"

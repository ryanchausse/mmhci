"""
Model
  - Note
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Note(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField()
    type = models.TextField()
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"Note Type: {self.type}"

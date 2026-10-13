"""
Model
  - Note
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Note(CreatedAndUpdatedBase):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    content = models.TextField()

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.type

"""
Model
  - Tag

Expect relations in many tables pointing to this model (e.g. PersonTag)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Tag(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField()
    content = models.TextField()

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f"Tag Name: {self.name}"

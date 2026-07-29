"""
Models
- Tag

Expect relations in many tables from this model (e.g. ContactTag)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Tag(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f"Tag Name: {self.name}"

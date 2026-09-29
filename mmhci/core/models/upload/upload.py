"""
Model
  - Upload
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Upload(CreatedAndUpdatedBase):
    name = models.TextField()
    type = models.TextField()
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    file_location = models.TextField()

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Upload"
        verbose_name_plural = "Uploads"

    def __str__(self):
        return f"Upload Name: {self.name} Type: {self.type}"

"""
Model
  - Upload
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Upload(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    type = models.TextField()
    description = models.TextField()
    content = models.TextField()
    file_location = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Upload"
        verbose_name_plural = "Uploads"

    def __str__(self):
        return f"Upload Name: {self.name} Type: {self.type}"

"""
Model
  - ContactUpload (relational)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class ContactUpload(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    contact = models.ForeignKey("core.Contact", on_delete=models.PROTECT)
    description = models.TextField()
    upload = models.ForeignKey("core.Upload", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactUpload"
        verbose_name_plural = "ContactUpload"

    def __str__(self):
        return f"Contact: {self.contact}, Upload: {self.upload}"

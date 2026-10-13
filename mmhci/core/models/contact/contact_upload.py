"""
Model
  - ContactUpload (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ContactUpload(CreatedAndUpdatedBase):
    name = models.TextField()
    contact = models.ForeignKey("core.Contact", on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    upload = models.ForeignKey("core.Upload", on_delete=models.PROTECT)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "ContactUpload"
        verbose_name_plural = "ContactUpload"

    def __str__(self):
        return f"{self.contact} - {self.upload}"

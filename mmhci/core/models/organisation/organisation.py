"""
Model
  - Organisation
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Organisation(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self):
        return f"Organisation Name: {self.name}"

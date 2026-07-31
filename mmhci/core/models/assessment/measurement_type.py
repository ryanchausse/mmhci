"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - MeasurementType (metadata table)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class MeasurementType(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField()

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "MeasurementType"
        verbose_name_plural = "MeasurementTypes"

    def __str__(self):
        return f"MeasurementType Name: {self.name}"

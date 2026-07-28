"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - MeasurementType (metadata table)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class MeasurementType(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "MeasurementType"
        verbose_name_plural = "MeasurementTypes"

    def __str__(self):
        return f"MeasurementType Name: {self.name}"

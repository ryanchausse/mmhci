"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - Assessment (main record of all Assessments performed)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


# This directory is for assessment models (IAR-DST, K10+, Surveys)
class Assessment(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(
        "core.AssessmentType", on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        return f"Assessment Name: {self.name}"

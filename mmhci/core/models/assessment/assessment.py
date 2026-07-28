"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - Assessment (main record of all Assessments performed)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


# This directory is for assessment models (IAR-DST, K10+, Surveys)
class Assessment(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    type = models.ForeignKey(
        "core.AssessmentType", on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        return f"Assessment Name: {self.name}"

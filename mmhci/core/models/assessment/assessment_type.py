"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - AssessmentType (metadata table)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class AssessmentType(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "AssessmentType"
        verbose_name_plural = "AssessmentTypes"

    def __str__(self):
        return f"AssessmentType Name: {self.name}"

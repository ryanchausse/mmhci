"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - AssessmentType (metadata table)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class AssessmentType(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "AssessmentType"
        verbose_name_plural = "AssessmentTypes"

    def __str__(self):
        return f"AssessmentType Name: {self.name}"

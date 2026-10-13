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
        verbose_name = "AssessmentType"
        verbose_name_plural = "AssessmentTypes"

    def __str__(self):
        return self.name

"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - AssessmentTypeMeasurementType (metadata/relational, enumerates Measurement Types
  for an Assessment type. Needed to construct Assessments.)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


# Relational
class AssessmentTypeMeasurementType(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    assessment_type = models.ForeignKey(
        "core.AssessmentType", on_delete=models.PROTECT
    )
    measurement_type = models.ForeignKey(
        "core.MeasurementType", on_delete=models.PROTECT
    )

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "MeasurementTypeAssessmentType"
        verbose_name_plural = "MeasurementTypeAssessmentTypes"

    def __str__(self):
        return (
            f"{self.assessment_type} - {self.measurement_type}"
        )

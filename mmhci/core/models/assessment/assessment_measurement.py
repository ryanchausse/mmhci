"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - AssessmentMeasurement (relational, links an Assessment to its Measurements)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


# Relational
class AssessmentMeasurement(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    assessment = models.ForeignKey("core.Assessment", on_delete=models.PROTECT)
    measurement = models.ForeignKey("core.Measurement", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "AssessmentMeasurement"
        verbose_name_plural = "AssessmentMeasurements"

    def __str__(self):
        return (
            f"AssessmentMeasurement Assessment: {self.assessment} - "
            f"Measurement: {self.measurement}"
        )

"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - Measurement (actual measured values)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


# generalisable for Likert / numerical scores, some qualitative
class Measurement(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    type = models.ForeignKey(
        "assessment.MeasurementType", on_delete=models.PROTECT, null=True, blank=True
    )
    # This table stores the actual measurement values. To make it generalisable, we
    # need to support all possible field types
    value_text = models.TextField()
    value_int = models.IntegerField(null=True, blank=True)
    value_bool = models.BooleanField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_decimal = models.DecimalField(
        decimal_places=50, max_digits=100, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"

    def __str__(self):
        return f"Measurement Name: {self.name}"

"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - Measurement (actual measured values)
"""

from django.db import models
from django.db.models import Q

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


# generalisable for Likert / numerical scores, some qualitative
class Measurement(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(
        "core.MeasurementType", on_delete=models.PROTECT, null=True, blank=True
    )
    # This table stores the actual measurement values. To make it generalisable, we
    # need to support all possible field types, but one must be filled in
    value_text = models.TextField(null=True, blank=True)
    value_int = models.IntegerField(null=True, blank=True)
    value_bool = models.BooleanField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_decimal = models.DecimalField(
        decimal_places=50, max_digits=100, null=True, blank=True
    )

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"
        constraints = [
            models.CheckConstraint(
                condition=Q(value_text__isnull=False) |
                          Q(value_int__isnull=False) |
                          Q(value_bool__isnull=False) |
                          Q(value_float__isnull=False) |
                          Q(value_decimal__isnull=False),
                name='at_least_one_value_must_be_supplied'
            )
        ]

    def __str__(self):
        return self.name

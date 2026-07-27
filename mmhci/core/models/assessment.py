"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Models
- Assessment (actual values)
- AssessmentMeasurement (relational, links an assessment to its measurements)
- AssessmentType (metadata table)
- AssessmentReferral (relational, links an assessment to a Referral)
- AssessmentTypeMeasurementType (metadata/relation, enumerates measurement types for an
                                 assessment type. Needed to construct assessments.)
- Measurement (actual values)
- MeasurementType (metadata table)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


# Assessment models (IAR-DST, K10+, Surveys)
class Assessment(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    type = models.ForeignKey(
        "assessment.AssessmentType", on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        return f"Assessment Name: {self.name}"


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


# Measurement models (generalisable for Likert / numerical scores, some qualitative)
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


# Relational
class AssessmentReferral(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    assessment = models.ForeignKey("assessment.Assessment", on_delete=models.PROTECT)
    referral = models.ForeignKey("referral.Referral", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "AssessmentReferral"
        verbose_name_plural = "AssessmentReferrals"

    def __str__(self):
        return (
            f"AssessmentReferral assessment: {self.assessment} - "
            f"referral {self.referral}"
        )


class AssessmentMeasurement(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    assessment = models.ForeignKey("assessment.Assessment", on_delete=models.PROTECT)
    measurement = models.ForeignKey("assessment.Measurement", on_delete=models.PROTECT)

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


class AssessmentTypeMeasurementType(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    assessment_type = models.ForeignKey(
        "assessment.AssessmentType", on_delete=models.PROTECT
    )
    measurement_type = models.ForeignKey(
        "assessment.MeasurementType", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "MeasurementTypeAssessmentType"
        verbose_name_plural = "MeasurementTypeAssessmentTypes"

    def __str__(self):
        return (
            f"AssessmentTypeMeasurementType: Assessment Type: {self.assessment_type} - "
            f"Measurement Type: {self.measurement_type}"
        )

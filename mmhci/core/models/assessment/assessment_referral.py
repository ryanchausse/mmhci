"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - AssessmentReferral (relational, links an Assessment to a Referral)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


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

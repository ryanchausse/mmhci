"""
Risk Assessment / IAR-DST / K10+ / K5 / SDQ
Model
  - AssessmentReferral (relational, links an Assessment to a Referral)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


# Relational
class AssessmentReferral(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    assessment = models.ForeignKey("core.Assessment", on_delete=models.PROTECT)
    referral = models.ForeignKey("core.Referral", on_delete=models.PROTECT)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "AssessmentReferral"
        verbose_name_plural = "AssessmentReferrals"

    def __str__(self):
        return (
            f"{self.assessment} - {self.referral}"
        )

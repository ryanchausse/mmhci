"""
Model
  - ReferralConsent (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ReferralConsent(CreatedAndUpdatedBase):
    referral = models.ForeignKey("core.Referral", on_delete=models.PROTECT)
    consent = models.ForeignKey("core.Consent", on_delete=models.PROTECT)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "ReferralConsent"
        verbose_name_plural = "ReferralConsent"

    def __str__(self):
        return f"{self.referral} - {self.consent}"

"""
Model
  - ReferralContact (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ReferralContact(CreatedAndUpdatedBase):
    referral = models.ForeignKey("core.Referral", on_delete=models.PROTECT)
    contact = models.ForeignKey("core.Contact", on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "ReferralContact"
        verbose_name_plural = "ReferralContact"

    def __str__(self):
        return f"{self.referral} - {self.contact}"

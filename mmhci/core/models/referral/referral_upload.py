"""
Model
  - ReferralUpload (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ReferralUpload(CreatedAndUpdatedBase):
    referral = models.ForeignKey("core.Referral", on_delete=models.PROTECT)
    upload = models.ForeignKey("core.Upload", on_delete=models.PROTECT)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "ReferralUpload"
        verbose_name_plural = "ReferralUpload"

    def __str__(self):
        return f"{self.referral} - {self.upload}"

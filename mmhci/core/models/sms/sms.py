"""
Model
  - Sms
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Sms(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    # Might want to make nullable due to SmsTemplate relation?
    content = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "SMS"
        verbose_name_plural = "SMSes"

    def __str__(self):
        return self.name

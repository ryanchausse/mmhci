"""
Model
  - Sms
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Sms(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    # Might want to make nullable due to SmsTemplate relation?
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "SMS"
        verbose_name_plural = "SMSes"

    def __str__(self):
        return f"SMS Name: {self.name}"

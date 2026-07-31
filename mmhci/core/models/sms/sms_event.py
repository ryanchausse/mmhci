"""
Model
  - SmsEvent (mainly sent SMSes)
"""

from django.conf import settings
from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class SmsEvent(CreatedAndUpdatedBase):
    sms = models.ForeignKey("core.Sms", on_delete=models.PROTECT)
    # A few different options for "to whom". Later, maybe add a constraint that checks
    # if at least one of the following three FKs are non-null
    sent_to_person = models.ForeignKey(
        "core.Person", on_delete=models.PROTECT, null=True, blank=True
    )
    sent_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )
    sent_to_practitioner = models.ForeignKey(
        "core.Practitioner", on_delete=models.PROTECT, null=True, blank=True
    )
    sent_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "SmsEvent"
        verbose_name_plural = "SmsEvents"

    def __str__(self):
        return f"SmsEvent SMS: {self.sms} - Sent At: {self.sent_at}"

"""
Models
- Sms
- SmsEvent (sent SMSes)
- SmsFormTemplate
"""

from django.conf import settings
from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Sms(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    # Might want to make nullable due to SmsTemplate relation
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "SMS"
        verbose_name_plural = "SMSes"

    def __str__(self):
        return f"SMS Name: {self.name}"


class SmsEvent(CreatedAndUpdatedMetaModel):
    sms = models.ForeignKey("sms.Sms", on_delete=models.PROTECT)
    # A few different options for "to whom"
    sent_to_person = models.ForeignKey(
        "person.Person", on_delete=models.PROTECT, null=True, blank=True
    )
    sent_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )
    sent_to_practitioner = models.ForeignKey(
        "practitioner.Practitioner", on_delete=models.PROTECT, null=True, blank=True
    )
    sent_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "SmsEvent"
        verbose_name_plural = "SmsEvents"

    def __str__(self):
        return f"SmsEvent SMS: {self.sms} - Sent At: {self.sent_at}"


# Relational
class SmsFormTemplate(CreatedAndUpdatedMetaModel):
    sms = models.ForeignKey("sms.Sms", on_delete=models.PROTECT)
    form_template = models.ForeignKey(
        "form_template.FormTemplate", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "SmsFormTemplate"
        verbose_name_plural = "SmsFormTemplate"

    def __str__(self):
        return f"SmsFormTemplate SMS: {self.sms} - FormTemplate: {self.form_template}"

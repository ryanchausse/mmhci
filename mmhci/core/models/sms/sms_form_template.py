"""
Model
  - SmsFormTemplate (relational)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class SmsFormTemplate(CreatedAndUpdatedMetaModel):
    sms = models.ForeignKey("core.Sms", on_delete=models.PROTECT)
    form_template = models.ForeignKey(
        "core.FormTemplate", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "SmsFormTemplate"
        verbose_name_plural = "SmsFormTemplate"

    def __str__(self):
        return f"SmsFormTemplate SMS: {self.sms} - FormTemplate: {self.form_template}"

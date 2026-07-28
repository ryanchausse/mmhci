"""
Model
  - FormTemplate

Might extend this to allow for FormTemplateItems, but the structure needs to be very
flexible as it's unclear how it should be organised at this time
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class FormTemplate(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    # Allow storage of text or to make use of JSON optimisation/structure
    content_text = models.TextField()
    content_json = models.JSONField(default=dict, null=True, blank=True)
    shareable = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "FormTemplate"
        verbose_name_plural = "FormTemplates"

    def __str__(self):
        return f"FormTemplate name: {self.name}"

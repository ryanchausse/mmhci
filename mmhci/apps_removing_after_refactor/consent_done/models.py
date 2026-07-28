"""
Models
- Consent
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Consent(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    # Don't default to False because it would make unclear if the value is affirmative
    given = models.BooleanField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Consent"
        verbose_name_plural = "Consents"

    def __str__(self):
        return f"Consent Description: {self.description}"

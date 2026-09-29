"""
Models
- Consent
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Consent(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    # Don't default to False because it would make unclear if the value is affirmative
    given = models.BooleanField()

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Consent"
        verbose_name_plural = "Consents"

    def __str__(self):
        return f"Consent Description: {self.description}"

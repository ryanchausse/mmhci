"""
Models
- Log

Probably needs more metadata, but we have relational tables like ModelLog we can utilise
"""

from django.conf import settings
from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Log(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    type = models.TextField()
    content = models.TextField()
    # For targeting a user other than the one creating the Log
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        return f"Log Type: {self.type}"

"""
Model
  - Log

Probably needs more metadata. We have relational tables like "Model"Log we can utilise
"""

from django.conf import settings
from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Log(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField()
    type = models.TextField()
    content = models.TextField()
    # For targeting a user other than the one creating the Log
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        return f"Log Type: {self.type}"

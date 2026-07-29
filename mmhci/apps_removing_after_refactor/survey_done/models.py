"""
Models
- Survey

Possibly add a relation for Survey <-> Assessment
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Survey(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return f"Survey Name: {self.name}"

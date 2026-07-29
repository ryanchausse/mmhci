"""
Models
- Role
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Role(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return f"Role Name: {self.name}"

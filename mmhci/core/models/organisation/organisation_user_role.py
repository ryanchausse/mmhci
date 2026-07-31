"""
Model
  - OrganisationUserRole (relational)
"""

from django.conf import settings
from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationUserRole(CreatedAndUpdatedBase):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    role = models.ForeignKey("core.Role", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationUserRole"
        verbose_name_plural = "OrganisationUserRoles"

    def __str__(self):
        return (
            f"OrganisationUserRole Organisation: {self.organisation} - "
            f"User: {self.user} - Role: {self.role}"
        )

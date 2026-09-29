"""
Model
  - OrganisationRole (relational)

This assigns 1:M permissions to each org "role", which is defined in this model.
There is not a Role base model; all roles are in an org context. In the future, perhaps
there will be global roles.
"""

from django.db import models
from django.contrib.auth.models import Permission

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationRole(CreatedAndUpdatedBase):
    permissions = models.ManyToManyField(
        Permission, blank=True, related_name="org_roles"
    )
    name = models.TextField()  # "Clinician", "Intake Administrator"
    description = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationRole"
        verbose_name_plural = "OrganisationRoles"

    def __str__(self):
        return (
            f"Name: {self.name} - "
            f"Permissions: {self.permissions}"
        )

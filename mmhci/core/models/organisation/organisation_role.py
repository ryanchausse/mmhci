"""
Model
  - OrganisationRole (relational)

NB: There is not a Role base model; all roles are in an org context.
"""

from django.db import models
from django.contrib.auth.models import Permission

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationRole(CreatedAndUpdatedBase):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT, related_name="roles"
    )
    name = models.TextField()  # "Clinician", "Intake Admin"
    # Connects to Django default Permissions object, which gets permissions from models
    # This is where specific permissions are assigned to roles in an organisation
    permissions = models.ManyToManyField(
        Permission, blank=True, related_name="organisation_roles"
    )

    class Meta(CreatedAndUpdatedBase.Meta):
        unique_together = ('organisation', 'name')
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationRole"
        verbose_name_plural = "OrganisationRoles"

    def __str__(self):
        return (
            f"OrganisationRole Organisation: {self.organisation} - "
            f"Name: {self.name} - Permissions: {self.permissions}"
        )

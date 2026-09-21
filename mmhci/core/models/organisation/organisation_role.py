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
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT, related_name="roles"
    )
    name = models.TextField()  # "Doctor", "Counselor", "Intake Administrator"
    # Connects to Django default Permissions object, which gets permissions from models
    # This is where specific permissions are assigned to roles in an organisation
    # Permissions should be defined in models wherever possible, if not, a "core"
    # permissions model, where complex service orchestration permissions can live, could
    # be defined. This plays nicely with things like migrations and Django's native
    # Permissions object. Will probably remove the OrgPermissionRequired mixin.
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

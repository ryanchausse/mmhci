"""
Model
  - OrganisationRole (relational)

This assigns 1:M permissions to each org "role", which is defined in this model.
There is not a Role base model; all roles are in an org context. In the future,
perhaps there will be global roles.
"""

from django.db import models
from django.contrib.auth.models import Permission

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationRole(CreatedAndUpdatedBase):
    # purposefully redundant for isolation and easy filtering
    organisation = models.ForeignKey(
        "core.Organisation",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="org_roles"
    )
    permissions = models.ManyToManyField(
        Permission, blank=True, related_name="org_roles"
    )
    name = models.TextField()  # "Clinician", "Intake Administrator"
    description = models.TextField(null=True, blank=True)

    @property
    def permission_list(self):
        return ", ".join(
            str(permission) for permission in self.permissions.all().values_list('name', flat=True)
        ) or "No permissions"

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["name"]
        verbose_name = "OrganisationRole"
        verbose_name_plural = "OrganisationRoles"

    def __str__(self):
        return (
            f"{self.name} - {self.organisation}"
        )

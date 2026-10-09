"""
Model
  - OrganisationGroup

This defines groups in orgs and associates org roles
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationGroup(CreatedAndUpdatedBase):
    organisation = models.ForeignKey(
        "core.Organisation",
        on_delete=models.PROTECT,
        related_name="org_groups"
    )
    roles = models.ManyToManyField(
        "core.OrganisationRole",
        blank=True,
        related_name="org_groups"
    )
    name = models.TextField()  # "Clinicians", "PHN Admins"

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["name"]
        verbose_name = "OrganisationGroup"
        verbose_name_plural = "OrganisationGroups"

    def __str__(self):
        roles = ", ".join(str(role) for role in self.roles.all()) or "No roles"
        return (
            f"Name: {self.name} "
            f"Organisation: {self.organisation} - "
            f"OrganisationRoles: {roles}"
        )

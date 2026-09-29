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
    role = models.ForeignKey(
        "core.OrganisationRole",
        on_delete=models.PROTECT,
        related_name="org_groups"
    )
    name = models.TextField()  # "Clinicians", "PHN Admins"

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationGroup"
        verbose_name_plural = "OrganisationGroups"

    def __str__(self):
        return (
            f"Name: {self.name} "
            f"Organisation: {self.organisation} - "
            f"OrganisationRole: {self.role}"
        )

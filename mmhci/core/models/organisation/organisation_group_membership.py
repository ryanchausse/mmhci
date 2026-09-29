"""
Model
  - OrganisationGroupMembership (relational)

This gives a User an Org Group association. Org Groups belong to Orgs.
"""

from django.conf import settings
from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationGroupMembership(CreatedAndUpdatedBase):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="org_group_memberships"
    )
    organisation_group = models.ForeignKey(
        "core.OrganisationGroup",
        on_delete=models.PROTECT,
        related_name="org_group_memberships"
    )
    description = models.TextField()

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationGroupMembership"
        verbose_name_plural = "OrganisationGroupMemberships"

    def __str__(self):
        return (
            f"OrganisationGroup: {self.organisation_group} - "
            f"User: {self.user}"
        )

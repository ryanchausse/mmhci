"""
Model
  - OrganisationGroupMembership (relational)

This gives a User an Org Group association. Org Groups belong to Orgs.
Consider changing to a multiple assignment-style model, as in OrganisationRole.
Leaving as a M:M relation for now mainly for ease of org-specific views and
assignment, but also for metadata purposes
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
    description = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "OrganisationGroupMembership"
        verbose_name_plural = "OrganisationGroupMemberships"

    def __str__(self):
        return (
            f"{self.user} - {self.organisation_group}"
        )

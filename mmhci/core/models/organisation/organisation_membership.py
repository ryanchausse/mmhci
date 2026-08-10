"""
Model
  - OrganisationMembership (relational)
"""

from django.conf import settings
from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationMembership(CreatedAndUpdatedBase):
    organisation_group = models.ForeignKey(
        "core.OrganisationGroup", on_delete=models.PROTECT, related_name="group_memberships"
    )
    organisation_role = models.ForeignKey(
        "core.OrganisationRole", on_delete=models.PROTECT, related_name="role_memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="user_memberships"
    )

    class Meta(CreatedAndUpdatedBase.Meta):
        unique_together = ('user', 'organisation_group')
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationMembership"
        verbose_name_plural = "OrganisationMembership"

    def __str__(self):
        return (
            f"OrganisationMembership OrganisationGroup: {self.organisation_group} - "
            f"User: {self.user} - Role: {self.organisation_role}"
        )

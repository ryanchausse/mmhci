"""
Model
  - OrganisationGroup
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationGroup(CreatedAndUpdatedBase):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT, related_name="groups"
    )
    name = models.TextField()  # "Clinicians", "PHN Admins"


    class Meta(CreatedAndUpdatedBase.Meta):
        unique_together = ('organisation', 'name')
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationGroup"
        verbose_name_plural = "OrganisationGroups"

    def __str__(self):
        return (
            f"OrganisationGroup Organisation: {self.organisation} - "
            f"Name: {self.name}"
        )

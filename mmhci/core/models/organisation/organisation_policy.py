"""
Model
  - OrganisationPolicy (relational)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class OrganisationPolicy(CreatedAndUpdatedMetaModel):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    policy = models.ForeignKey("core.Policy", on_delete=models.PROTECT)


    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationPolicy"
        verbose_name_plural = "OrganisationPolicies"

    def __str__(self):
        return (
            f"OrganisationPolicy Organisation: {self.organisation} - "
            f"Policy: {self.policy}"
        )

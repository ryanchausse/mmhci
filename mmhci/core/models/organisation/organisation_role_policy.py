"""
Model
  - OrganisationRolePolicy (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationRolePolicy(CreatedAndUpdatedBase):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    role = models.ForeignKey("core.Role", on_delete=models.PROTECT)
    policy = models.ForeignKey("core.Policy", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationRolePolicy"
        verbose_name_plural = "OrganisationRolePolicies"

    def __str__(self):
        return (
            f"OrganisationRolePolicy Organisation: {self.organisation} - "
            f"Policy: {self.policy} - Role: {self.role}"
        )

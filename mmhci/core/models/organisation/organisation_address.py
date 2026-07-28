"""
Model
  - OrganisationAddress (relational)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class OrganisationAddress(CreatedAndUpdatedMetaModel):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    address = models.ForeignKey("core.Address", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationAddress"
        verbose_name_plural = "OrganisationAddresses"

    def __str__(self):
        return (
            f"OrganisationAddress Organisation: {self.organisation} - "
            f"Address: {self.address}"
        )

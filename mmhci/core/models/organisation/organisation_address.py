"""
Model
  - OrganisationAddress (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationAddress(CreatedAndUpdatedBase):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    address = models.ForeignKey("core.Address", on_delete=models.PROTECT)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "OrganisationAddress"
        verbose_name_plural = "OrganisationAddresses"

    def __str__(self):
        return (
            f"{self.organisation} - {self.address}"
        )

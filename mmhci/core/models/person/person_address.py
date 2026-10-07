"""
Model
  - PersonAddress (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class PersonAddress(CreatedAndUpdatedBase):
    person = models.ForeignKey(
        "core.Person", on_delete=models.PROTECT
    )
    address = models.ForeignKey("core.Address", on_delete=models.PROTECT)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "PersonAddress"
        verbose_name_plural = "PersonAddresses"

    def __str__(self):
        return (
            f"PersonAddress Person: {self.person} - "
            f"Address: {self.address}"
        )

"""
Model
  - PersonAddress (relational)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class PersonAddress(CreatedAndUpdatedMetaModel):
    person = models.ForeignKey(
        "core.Person", on_delete=models.PROTECT
    )
    address = models.ForeignKey("core.Address", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "PersonAddress"
        verbose_name_plural = "PersonAddresses"

    def __str__(self):
        return (
            f"PersonAddress Person: {self.person} - "
            f"Address: {self.address}"
        )

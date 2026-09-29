"""
Model
  - PractitionerAddress (relational)
"""

from django.db import models
from django.db.models import Q

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class PractitionerAddress(CreatedAndUpdatedBase):
    practitioner = models.ForeignKey(
        "core.Practitioner", on_delete=models.PROTECT
    )
    primary_address = models.ForeignKey("core.Address", on_delete=models.PROTECT, null=True, blank=True, related_name="practitioner_primary_addresses")
    mailing_address = models.ForeignKey("core.Address", on_delete=models.PROTECT, null=True, blank=True, related_name="practitioner_mailing_addresses")
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "PractitionerAddress"
        verbose_name_plural = "PractitionerAddresses"
        constraints = [
            models.CheckConstraint(
                condition=Q(primary_address__isnull=False) | Q(mailing_address__isnull=False),
                name='at_least_one_of_primary_or_mailing_address_must_be_supplied'
            )
        ]

    def __str__(self):
        return f"Practitioner Name: {self.name} - Address: {self.address}"

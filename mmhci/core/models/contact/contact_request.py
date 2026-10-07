"""
Model
  - ContactRequest (formerly "CallbackRequest")
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ContactRequest(CreatedAndUpdatedBase):
    contact = models.ForeignKey(
        "core.Contact", on_delete=models.PROTECT, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    # There should be a FK to an "Availability" model that represents the best days
    # and times to call a Person. This might involve a few tables:
    # - days_of_week
    # - availability_hours (FK to days_of_week and Person)
    # - possibly a date_overrides table for exceptions to availability

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "ContactRequest"
        verbose_name_plural = "ContactRequests"

    def __str__(self):
        return f"ContactRequest Contact: {self.contact}, Method: {self.method}"

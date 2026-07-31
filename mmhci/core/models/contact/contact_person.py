"""
Model
  - ContactPerson (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ContactPerson(CreatedAndUpdatedBase):
    contact = models.ForeignKey("core.Contact", on_delete=models.PROTECT)
    description = models.TextField()
    person = models.ForeignKey("core.Person", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactPerson"
        verbose_name_plural = "ContactPeople"

    def __str__(self):
        return f"Contact: {self.contact}, Person: {self.person}"

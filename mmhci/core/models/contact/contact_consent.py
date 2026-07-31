"""
Model
  - ContactConsent (relational)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class ContactConsent(CreatedAndUpdatedBase):
    contact = models.ForeignKey("core.Contact", on_delete=models.PROTECT)
    consent = models.ForeignKey("core.Consent", on_delete=models.PROTECT)
    description = models.TextField()
    # Although Contact contains an FK to Person/ContactPerson, they could be NULL
    person = models.ForeignKey("core.Person", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactConsent"
        verbose_name_plural = "ContactConsents"

    def __str__(self):
        return f"Contact: {self.contact}, Consent: {self.consent}"

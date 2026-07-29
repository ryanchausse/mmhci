"""
Models
- Practitioner
- PractitionerAddress
- PractitionerOrganisation
"""

from django.conf import settings
from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Practitioner(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    # Practitioner possibly has a user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )
    phone = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Practitioner"
        verbose_name_plural = "Practitioners"

    def __str__(self):
        return f"Practitioner Name: {self.name}"


# Relational
class PractitionerAddress(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    primary = models.BooleanField()
    mailing = models.BooleanField()
    practitioner = models.ForeignKey(
        "practitioner.Practitioner", on_delete=models.PROTECT
    )
    address = models.ForeignKey("core.Address", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "PractitionerAddress"
        verbose_name_plural = "PractitionerAddresses"

    def __str__(self):
        return f"Practitioner Name: {self.name} - Address: {self.address}"


class PractitionerOrganisation(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    practitioner = models.ForeignKey(
        "practitioner.Practitioner", on_delete=models.PROTECT
    )
    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "PractitionerOrganisation"
        verbose_name_plural = "PractitionerOrganisations"

    def __str__(self):
        return f"Practitioner Name: {self.name} - Organisation: {self.organisation}"

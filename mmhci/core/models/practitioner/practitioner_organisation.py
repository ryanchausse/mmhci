"""
Model
  - PractitionerOrganisation (relational)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class PractitionerOrganisation(CreatedAndUpdatedMetaModel):
    practitioner = models.ForeignKey(
        "core.Practitioner", on_delete=models.PROTECT
    )
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "PractitionerOrganisation"
        verbose_name_plural = "PractitionerOrganisations"

    def __str__(self):
        return f"Practitioner Name: {self.name} - Organisation: {self.organisation}"

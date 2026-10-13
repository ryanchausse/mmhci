"""
Model
  - OrganisationFormTemplate
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class OrganisationFormTemplate(CreatedAndUpdatedBase):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    form_template = models.ForeignKey(
        "core.FormTemplate", on_delete=models.PROTECT
    )

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "OrganisationFormTemplate"
        verbose_name_plural = "OrganisationFormTemplates"

    def __str__(self):
        return (
            f"{self.organisation} - {self.form_template}"
        )

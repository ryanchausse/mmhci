"""
Model
  - OrganisationFormTemplate
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class OrganisationFormTemplate(CreatedAndUpdatedMetaModel):
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT
    )
    form_template = models.ForeignKey(
        "core.FormTemplate", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationFormTemplate"
        verbose_name_plural = "OrganisationFormTemplates"

    def __str__(self):
        return (
            f"OrganisationFormTemplate Organisation: {self.organisation} - "
            f"FormTemplate: {self.form_template}"
        )

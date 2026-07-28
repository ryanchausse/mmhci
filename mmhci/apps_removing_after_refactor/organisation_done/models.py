"""
Models
- Organisation
- OrganisationAddress
- OrganisationPolicy
- OrganisationRolePolicy
- OrganisationUserRole
- OrganisationFormTemplate
"""

from django.conf import settings
from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Organisation(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self):
        return f"Organisation Name: {self.name}"


# Relational
class OrganisationAddress(CreatedAndUpdatedMetaModel):
    address = models.ForeignKey("core.Address", on_delete=models.PROTECT)
    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationAddress"
        verbose_name_plural = "OrganisationAddresses"

    def __str__(self):
        return (
            f"OrganisationAddress Organisation: {self.organisation} - "
            f"Address: {self.address}"
        )


class OrganisationPolicy(CreatedAndUpdatedMetaModel):
    policy = models.ForeignKey("policy.Policy", on_delete=models.PROTECT)
    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationPolicy"
        verbose_name_plural = "OrganisationPolicies"

    def __str__(self):
        return (
            f"OrganisationPolicy Organisation: {self.organisation} - "
            f"Policy: {self.policy}"
        )


class OrganisationRolePolicy(CreatedAndUpdatedMetaModel):
    policy = models.ForeignKey("policy.Policy", on_delete=models.PROTECT)
    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.PROTECT
    )
    role = models.ForeignKey("role.Role", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationRolePolicy"
        verbose_name_plural = "OrganisationRolePolicies"

    def __str__(self):
        return (
            f"OrganisationRolePolicy Organisation: {self.organisation} - "
            f"Policy: {self.policy} - Role: {self.role}"
        )


class OrganisationUserRole(CreatedAndUpdatedMetaModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.PROTECT
    )
    role = models.ForeignKey("role.Role", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "OrganisationUserRole"
        verbose_name_plural = "OrganisationUserRoles"

    def __str__(self):
        return (
            f"OrganisationUserRole Organisation: {self.organisation} - "
            f"User: {self.user} - Role: {self.role}"
        )


class OrganisationFormTemplate(CreatedAndUpdatedMetaModel):
    form_template = models.ForeignKey(
        "form_template.FormTemplate", on_delete=models.PROTECT
    )
    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.PROTECT
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

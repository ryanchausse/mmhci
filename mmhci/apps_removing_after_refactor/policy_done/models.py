"""
Models
- Policy
- Resource (maybe, meant to define what object and parameters (e.g. Person.first_name)
            a role has access to by policy and create/read/update/delete. Maybe this
            should be defined in a table like OrganisationRolePolicy instead? Or can
            make this generalised, recording a Resource's model/field and access method)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Policy(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return f"Policy Name: {self.name}"


# This will evolve
class Resource(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self):
        return f"Resource Name: {self.name}"


# Relational
class PolicyResource(CreatedAndUpdatedMetaModel):
    policy = models.ForeignKey("policy.Policy", on_delete=models.PROTECT)
    resource = models.ForeignKey("policy.Resource", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "PolicyResource"
        verbose_name_plural = "PolicyResources"

    def __str__(self):
        return f"PolicyResource Policy: {self.policy} - Resource: {self.resource}"

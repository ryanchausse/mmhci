from django.db import models
from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


# This is a helper model that is exclusively used to arbitrarily define all
# needed permissions that can't live in any particular model. Because
# of the way Django's Permissions works, permissions are derived from
# or defined in model instances. This is kind of kludgey but will work ok
# for now - see permissions in subclass Meta.
class OrchestrationPermissions(CreatedAndUpdatedBase):
    name = models.TextField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "OrchestrationPermissions"
        verbose_name_plural = "OrchestationPermissions"

        permissions = [
            (
                'can_run_orchestration',
                'Can run any orchestrated services'
            ),
            (
                'can_change_referral_owner',
                'Can run the orchestration that changes the assigned referral '
                'owner org and emails the relevant person at the new org'
            ),
        ]

    def __str__(self):
        return f"OrchestrationPermissions helper class. Do not use."

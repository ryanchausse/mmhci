"""
Model
  - Policy

This will likely be replaced with a combination of native Django user groups and
has_perm(), which benefits from native cacheing of all permissions during an HTTP
request cycle when the first permission is queried.

There could be middleware on all Views to restrict them similar to the @login_required
decorator, then a custom rules engine as a Mixin for the combination of Organisation,
User, Role, and Policy, with permissions (like the natively assigned "app.create_model",
"app.update_model", etc.) defined in the model.

Custom permissions can also be assigned this way and assigned and checked in either
services or views (prob need to choose one of those two as a standard).

Models should include required fields for the mixin, like:
permissions_required = ["app.view_client", "can_transfer_to_another_org", ...]
and so on.

Permissions can be assigned using Django-native model definitions under the Meta class,
but they don't reach the level of rules engine that we may need for a per-model and also
per-field permission check. We could be careful and sort out permissions for each
view or service action, but I want to make this really hard to mess up by forgetting
to do so. The only way that springs to mind right now is to use inheritance or
composition that requires necessary fields to be supplied / overridden, with a deny by
default posture.

There are packages, such as django-guardian, I believe, that enforce per-instance in
addition to model/field restrictions, but that type of system would create a huge amount
of data as part of our normal operations / JOINs on any action.

Side note, this is similar to our need to log reads of data, but I think we should just
custom define which reads are necessary to record in our views themselves instead of a
global mechanism for that.

check out:
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Policy(CreatedAndUpdatedBase):
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

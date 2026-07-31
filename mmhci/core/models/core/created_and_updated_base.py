"""
Model:
  - CreatedAndUpdatedBase
    - Inherits from default Django model and adds created/updated at and by
    - Creates fields like "[appname_]fkmodelname_updated_by" on the User table
      - To find all Roles updated by a User, we can do (get AUTH_USER_MODEL IRL):
        User.objects.get(id=1).role_role_updated_by.all()
      - This can also be queried using the relational tables, which could be
        write redundant in some event stream/logging contexts, but maintaining these
        FK relations could be more performant when querying the model directly.
        e.g. we could query the updated_by a given model, but relational tables can be
        JOINed to and queried in other contexts (e.g. "find all updates to a Role
        record").
      - There is also no/minimal performance cost to doing it this way as these
        relations are mapped in memory. The User table will have a lot of hidden
        fields/properties however.
"""

from django.conf import settings
from django.db import models

class CreatedAndUpdatedBase(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

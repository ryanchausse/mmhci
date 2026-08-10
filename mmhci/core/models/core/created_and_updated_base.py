"""
Model:
  - CreatedAndUpdatedBase
    - Inherits from default Django model and adds created/updated at and by
    - Creates fields like "[appname_]fkmodelname_updated_by" on the User table
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

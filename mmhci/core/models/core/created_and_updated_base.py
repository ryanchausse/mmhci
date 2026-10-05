"""
Model:
  - CreatedAndUpdatedBase
    - Creates fields like "[appname_]fkmodelname_updated_by" on the User table
      - There is also no/minimal performance cost to doing it this way as these
        relations are mapped in memory.
"""

from django.conf import settings
from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class CreatedAndUpdatedBase(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=['is_deleted'])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    owning_organisation = models.ForeignKey(
        "core.Organisation",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_owning_org"
    )
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

"""
These are core models that should be part of the overall project/repo/web app. They
should be widely used by different apps and are therefore located here. They could also
possibly be so complex, orchestrating many objects, that they don't belong in any one
app / domain / bounded context. Core infrastructure should be located here also, like
UI / main templates / certain static assets / etc. Still, this app should be really
lightly used to prevent coupling and circular dependencies.

Add a mixin model via pip package django-simple-history?

Models:
- CreatedAndUpdatedMetaModel
  - Inherits from default Django model and adds created/updated at and by
  - Creates fields like "appname_fkmodelname_updated_by" on the User table
    - To find all Roles updated by a User, we can do (get AUTH_USER_MODEL IRL):
        User.objects.get(id=1).role_role_updated_by.all()
      This could be a little confusing as the app name might be the same as the FK model
      name [%(app_label)s], but we need that field namespace to be unique.
    - This can also be queried using the relational tables, and can be write-redundant,
      but maintaining this relation could be more performant on querying
      for, say, the updated_by on one record, whereas relational tables can be
      JOINed to and queried in other contexts for event stream-like usage (e.g.
      find all updates to a Role record). For some models, there would be an audit log
      entry too. Currently considering integrating django-simple-history as well.
    - We don't need to worry about the app name registered in apps.py being long (e.g.
      "mmhci.apps.role" because Django just creates a handle based on
      the last part of the name, in this case "role").
    - There is also no performance cost to doing it this way as these relations are
      mapped in memory. The User table will have a lot of hidden fields/properties
      however.
- Address
- Announcement
"""

from django.conf import settings
from django.db import models


class CreatedAndUpdatedMetaModel(models.Model):
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


class Address(CreatedAndUpdatedMetaModel):
    address_line1 = models.TextField()
    address_line2 = models.TextField(blank=True)
    address_line3 = models.TextField(blank=True)
    city = models.TextField()
    state = models.TextField()
    country = models.TextField(default="AU", max_length=2)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"Address Line 1: {self.address_line1}"


class Announcement(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    content = models.TextField()
    active = models.BooleanField(default=True)
    start = models.DateTimeField(null=True)
    expiry = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return f"Announcement Name: {self.name}"

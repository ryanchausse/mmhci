from django.db import models
from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


class Announcement(CreatedAndUpdatedBase):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    active = models.BooleanField(default=True)
    start = models.DateTimeField(null=True)
    expiry = models.DateTimeField(null=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.name

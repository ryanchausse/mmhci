"""
Model
  - ReferralEvent ("ReferredTo" in our current system, sort of?)
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase

# Enum. Move to another location. Duplicated in Referral model
class Statuses(models.IntegerChoices):
    NEW = 0, "New"
    IN_PROGRESS = 1, "In Progress"
    ABANDONED = 2, "Abandoned"
    COMPLETED = 3, "Completed"
    SENT = 4, "Sent"
    ACCEPTED = 5, "Accepted"

# Enum. Move to another location.
class EventTypes(models.IntegerChoices):
    ORIGINATED = 0, "Originated"
    ASSIGNED = 1, "Assigned"
    STATUS_CHANGED = 2, "Status Changed"


class ReferralEvent(CreatedAndUpdatedBase):
    referral = models.ForeignKey("core.Referral", on_delete=models.PROTECT)
    organisation = models.ForeignKey(
        "core.Organisation", on_delete=models.PROTECT, null=True, blank=True
    )
    practitioner = models.ForeignKey(
        "core.Practitioner", on_delete=models.PROTECT, null=True, blank=True
    )
    event_type = models.IntegerField(choices=EventTypes, null=True, blank=True)
    status = models.IntegerField(choices=Statuses, null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "ReferralEvent"
        verbose_name_plural = "ReferralEvent"

    def __str__(self):
        return (
            f"{self.referral} - "
            f"{self.organisation} - "
            f"{self.practitioner} - "
            f"{self.type} - "
            f"{self.status}"
        )

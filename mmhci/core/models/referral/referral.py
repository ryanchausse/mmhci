"""
Model
  - Referral
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase

# Enum. Move to another location.
class Statuses(models.IntegerChoices):
    NEW = 0, "New"
    IN_PROGRESS = 1, "In Progress"
    ABANDONED = 2, "Abandoned"
    COMPLETED = 3, "Completed"
    SENT = 4, "Sent"
    ACCEPTED = 5, "Accepted"


class Referral(CreatedAndUpdatedBase):
    org_originated = models.ForeignKey(
        "core.Organisation",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_originated",
    )
    org_assigned = models.ForeignKey(
        "core.Organisation",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_assigned",
    )
    org_owner = models.ForeignKey(
        "core.Organisation",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_owned",
    )
    practitioner_originated = models.ForeignKey(
        "core.Practitioner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_originated",
    )
    practitioner_assigned = models.ForeignKey(
        "core.Practitioner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_assigned",
    )
    practitioner_owner = models.ForeignKey(
        "core.Practitioner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_owned",
    )
    name = models.TextField()
    description = models.TextField()
    # Intentionally duplicated vs. querying ReferralEvent which can return latest status
    status = models.IntegerField(choices=Statuses, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"

    def __str__(self):
        return f"Referral Name: {self.name}"

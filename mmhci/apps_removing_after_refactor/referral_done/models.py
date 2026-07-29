"""
NB: Still need to sort out how to record the Referral's "outcome" (e.g. Sent, Accepted)
Models
- Referral
- ReferralAuditLog (to record changes to the Referral UPDATE: change to use
                    django-simple-history pip package?)
- ReferralConsent
(The next few are represented formerly in "ReferredTo", might need to keep using that)
- ReferralPractitioner NO
- ReferralOrg (relational - initiated by org, owned by org, many entries possible) NO
- ReferralOrgStatus (relational - status by org but also contains changes over time) NO
- ReferralOrgPractitioner? Trying to find a replacement for ReferredTo YES
- ReferralStatus NO
- ReferralUpload

In the end, I think it might have to be ReferralOrgPractitioner, with the following
metadata fields:
- status
- org_originated (?)
- org_assigned
- org_owner
- practitioner_originated
- practitioner_assigned
- org_owner

This covers the following use cases:
- What's the referral status?
- Who owns the referral?
- When was the referral sent?
- Was the referral assigned to an org or a practitioner?
- When was the referral re-assigned?
- When the referral was sent, through which org was the practitioner working?
- What are the last 10 referrals that have been sent?
- Which orgs and practitioners was the referral sent to and when?
- Which orgs receive the most referrals?

It seems denormalised enough to prevent a gang of JOINs, but keep an eye on usage. Worst
case scenario is waiting for locks to be released, but that depends on load (I expect
very minimal) and query patterns (could be a problem if we're very uncautious)

Actually... I wonder, though, if this is an abuse of this system. Maybe
originated/assigned should live in the Referral table? ...yes, I am abusing this table.
At a minimum, status should go in the Referral table. Think about the bounded
context/domain.

The best situation might be to maintain an FK to the latest record in the
ReferralOrgPractitioner table within the Referral table, and record via INSERT all
changes made in the relational table itself.

Meh, keep it in the relational table and override save() when necessary for read query
performance. I think this will be good enough for now, and I don't want to violate the
pattern because I think the other devs might struggle with the whatever it is: database
trigger to update the field, or overridden save() method for just that one model, etc.
One other thing to keep in mind, however, is that the relational table is only getting
INSERTs. Hmm... It's kind of an event stream really. Maybe the history belongs in the
ReferralAuditLog table instead, with the latest status and assigned orgs/practitioners
in this relational table? But again, we have a problem because a Referral can have
multiple assigned orgs and practitioners. I suppose we could have new relational records
when a new org/practitioner is being referred to? But how to ensure this is not easy to
get wrong? We could not for example do something like "select latest referral record" to
get all assigned orgs... but that should be obvious anyway?

Update: just call the relational table ReferralEvent. It's similar to an event stream.
The current status is the latest record and previous status changes can be constructed
from analysis of every ReferralEvent record.

"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Referral(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    description = models.TextField()
    org_originated = models.ForeignKey(
        "organisation.Organisation",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_originated",
    )
    org_assigned = models.ForeignKey(
        "organisation.Organisation",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_assigned",
    )
    org_owner = models.ForeignKey(
        "organisation.Organisation",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_owned",
    )
    practitioner_originated = models.ForeignKey(
        "practitioner.Practitioner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_originated",
    )
    practitioner_assigned = models.ForeignKey(
        "practitioner.Practitioner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_assigned",
    )
    practitioner_owner = models.ForeignKey(
        "practitioner.Practitioner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referrals_owned",
    )

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"

    def __str__(self):
        return f"Referral Name: {self.name}"


# Enums
class Statuses(models.IntegerChoices):
    NEW = 0, "New"
    IN_PROGRESS = 1, "In Progress"
    ABANDONED = 2, "Abandoned"
    COMPLETED = 3, "Completed"
    SENT = 4, "Sent"
    ACCEPTED = 5, "Accepted"


class EventTypes(models.IntegerChoices):
    ORIGINATED = 0, "Originated"
    ASSIGNED = 1, "Assigned"
    STATUS_CHANGED = 3, "Status Changed"


# Relational
class ReferralEvent(CreatedAndUpdatedMetaModel):
    referral = models.ForeignKey("referral.Referral", on_delete=models.PROTECT)
    organisation = models.ForeignKey(
        "organisation.Organisation", on_delete=models.PROTECT, null=True, blank=True
    )
    practitioner = models.ForeignKey(
        "practitioner.Practitioner", on_delete=models.PROTECT, null=True, blank=True
    )
    event_type = models.IntegerField(choices=EventTypes, null=True, blank=True)
    status = models.IntegerField(choices=Statuses, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ReferralEvent"
        verbose_name_plural = "ReferralEvent"

    def __str__(self):
        return (
            f"ReferralEvent Referral: {self.referral} - "
            f"Organisation: {self.organisation} - Practitioner: {self.practitioner} - "
            f"Event Type: {self.type} - Status: {self.status}"
        )


class ReferralUpload(CreatedAndUpdatedMetaModel):
    referral = models.ForeignKey("referral.Referral", on_delete=models.PROTECT)
    upload = models.ForeignKey("upload.Upload", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ReferralUpload"
        verbose_name_plural = "ReferralUpload"

    def __str__(self):
        return f"ReferralUpload Referral: {self.referral} -  Upload: {self.upload}"

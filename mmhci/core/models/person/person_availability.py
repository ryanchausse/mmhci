"""
Model
  - PersonAvailability

This may change in terms of implementation - possibly a new Availability model
Might also add "exception to availability on a certain date(s)"
"""

from django.db import models

from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase


# Enums
class DaysOfWeek(models.IntegerChoices):
    MONDAY = 0, "Monday"
    TUESDAY = 1, "Tuesday"
    WEDNESDAY = 2, "Wednesday"
    THURSDAY = 3, "Thursday"
    FRIDAY = 4, "Friday"
    SATURDAY = 5, "Saturday"
    SUNDAY = 6, "Sunday"


class PersonAvailability(CreatedAndUpdatedBase):
    person = models.ForeignKey(
        "core.Person", on_delete=models.PROTECT, null=True, blank=True
    )
    day_of_week = models.IntegerField(choices=DaysOfWeek, null=True, blank=True)
    time_from = models.TimeField(null=True, blank=True)
    time_until = models.TimeField(null=True, blank=True)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "PersonAvailability"
        verbose_name_plural = "PersonAvailabilities"

    def __str__(self):
        return (
            f"Person: {self.person} "
            f"Availability: {self.day_of_week}: {self.time_from} - {self.time_until}"
        )

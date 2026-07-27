"""
Models
- Person
- PersonAddress
- PersonAuditLog (changes to demographic info over time, might replace with pip
                  package django-simple-history as middleware)
- PersonAvailability (relational)
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Person(CreatedAndUpdatedMetaModel):
    address = models.ForeignKey(
        "core.Address", on_delete=models.PROTECT, null=True, blank=True
    )
    # If last_name, or first_name/last_name/etc. become constrained as unique, we can
    # introduce null=True in these TextField()s
    first_name = models.TextField()
    last_name = models.TextField(blank=True)
    preferred_name = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    # Consider using pip package django-phonenumber-field. For now, be permissive.
    phone = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return (
            f"Person Name: {self.first_name} '{self.preferred_name}' {self.last_name}"
        )


# Enums
class DaysOfWeek(models.IntegerChoices):
    MONDAY = 0, "Monday"
    TUESDAY = 1, "Tuesday"
    WEDNESDAY = 2, "Wednesday"
    THURSDAY = 3, "Thursday"
    FRIDAY = 4, "Friday"
    SATURDAY = 5, "Saturday"
    SUNDAY = 6, "Sunday"


# Relational
class PersonAvailability(CreatedAndUpdatedMetaModel):
    person = models.ForeignKey(
        "person.Person", on_delete=models.PROTECT, null=True, blank=True
    )
    day_of_week = models.IntegerField(choices=DaysOfWeek, null=True, blank=True)
    time_from = models.TimeField(null=True, blank=True)
    time_until = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "PersonAvailability"
        verbose_name_plural = "PeopleAvailability"

    def __str__(self):
        return (
            f"Person: {self.person} "
            f"Availability: {self.day_of_week}: {self.time_from} - {self.time_until}"
        )

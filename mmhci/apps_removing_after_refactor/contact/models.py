"""
Models
- Contact (incoming)
- ContactAttempt (outgoing)
- ContactConsent
- ContactNote
- ContactPerson
- ContactRequest (formerly "CallbackRequest")
- ContactUpload
"""

from django.db import models

from mmhci.core.models import CreatedAndUpdatedMetaModel


class Contact(CreatedAndUpdatedMetaModel):
    description = models.TextField()
    person = models.ForeignKey(
        "person.Person", on_delete=models.PROTECT, null=True, blank=True
    )
    type = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"Contact Type: {self.type}"


class ContactAttempt(CreatedAndUpdatedMetaModel):
    contact = models.ForeignKey(
        "contact.Contact", on_delete=models.PROTECT, null=True, blank=True
    )
    description = models.TextField()
    method = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactAttempt"
        verbose_name_plural = "ContactAttempts"

    def __str__(self):
        return f"ContactAttempt Contact: {self.contact}, Method: {self.method}"


class ContactRequest(CreatedAndUpdatedMetaModel):
    contact = models.ForeignKey(
        "contact.Contact", on_delete=models.PROTECT, null=True, blank=True
    )
    description = models.TextField()
    method = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactRequest"
        verbose_name_plural = "ContactRequests"

    def __str__(self):
        return f"ContactRequest Contact: {self.contact}, Method: {self.method}"


# Relational
class ContactConsent(CreatedAndUpdatedMetaModel):
    contact = models.ForeignKey("contact.Contact", on_delete=models.PROTECT)
    consent = models.ForeignKey("consent.Consent", on_delete=models.PROTECT)
    description = models.TextField()
    person = models.ForeignKey("person.Person", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactConsent"
        verbose_name_plural = "ContactConsents"

    def __str__(self):
        return f"Contact: {self.contact}, Consent: {self.consent}"


class ContactNote(CreatedAndUpdatedMetaModel):
    name = models.TextField()
    contact = models.ForeignKey("contact.Contact", on_delete=models.PROTECT)
    description = models.TextField()
    note = models.ForeignKey("note.Note", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["created_at"]
        verbose_name = "ContactNote"
        verbose_name_plural = "ContactNotes"

    def __str__(self):
        return f"Contact: {self.contact}, Note: {self.note}"

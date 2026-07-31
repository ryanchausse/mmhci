from django.db import models
from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase

class Address(CreatedAndUpdatedBase):
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

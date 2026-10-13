from django.db import models
from mmhci.core.models.core.created_and_updated_base import CreatedAndUpdatedBase

class Address(CreatedAndUpdatedBase):
    address_line1 = models.TextField()
    address_line2 = models.TextField(blank=True)
    address_line3 = models.TextField(blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    country = models.TextField(default="AU", max_length=2)

    class Meta(CreatedAndUpdatedBase.Meta):
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return (
            f"{self.address_line1} - "
            f"{self.address_line2} - "
            f"{self.city} - "
            f"{self.state}"
        )

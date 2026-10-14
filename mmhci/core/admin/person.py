from django.contrib import admin

from mmhci.core.models.person import *

admin.site.register(PersonAddress)
admin.site.register(PersonAvailability)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = (
        "uuid", "created_at", "created_by", "updated_at", "updated_by"
    )

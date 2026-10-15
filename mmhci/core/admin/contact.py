from django.contrib import admin

from mmhci.core.models.contact import *

admin.site.register(ContactAttempt)
admin.site.register(ContactConsent)
admin.site.register(ContactNote)
admin.site.register(ContactPerson)
admin.site.register(ContactRequest)
admin.site.register(ContactUpload)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = (
        "uuid", "created_at", "created_by", "updated_at", "updated_by"
    )

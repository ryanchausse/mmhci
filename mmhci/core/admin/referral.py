from django.contrib import admin

from mmhci.core.models.referral import *

admin.site.register(ReferralConsent)
admin.site.register(ReferralEvent)
admin.site.register(ReferralUpload)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    readonly_fields = (
        "uuid", "created_at", "created_by", "updated_at", "updated_by"
    )

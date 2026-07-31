from django.contrib import admin

from mmhci.core.models.referral import referral_consent
from mmhci.core.models.referral import referral_event
from mmhci.core.models.referral import referral_upload
from mmhci.core.models.referral import referral

admin.site.register(referral_consent)
admin.site.register(referral_event)
admin.site.register(referral_upload)
admin.site.register(referral)

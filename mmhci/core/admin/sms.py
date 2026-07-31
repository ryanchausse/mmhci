from django.contrib import admin

from mmhci.core.models.sms import *

admin.site.register(SmsEvent)
admin.site.register(SmsFormTemplate)
admin.site.register(Sms)

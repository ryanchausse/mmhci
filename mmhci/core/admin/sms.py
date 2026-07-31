from django.contrib import admin

from mmhci.core.models.sms import sms_event
from mmhci.core.models.sms import sms_form_template
from mmhci.core.models.sms import sms

admin.site.register(sms_event)
admin.site.register(sms_form_template)
admin.site.register(sms)

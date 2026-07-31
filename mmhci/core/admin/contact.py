from django.contrib import admin

from mmhci.core.models.contact import contact
from mmhci.core.models.contact import contact_attempt
from mmhci.core.models.contact import contact_consent
from mmhci.core.models.contact import contact_note
from mmhci.core.models.contact import contact_person
from mmhci.core.models.contact import contact_request
from mmhci.core.models.contact import contact_upload

admin.site.register(contact_attempt)
admin.site.register(contact_consent)
admin.site.register(contact_note)
admin.site.register(contact_person)
admin.site.register(contact_request)
admin.site.register(contact_upload)
admin.site.register(contact)

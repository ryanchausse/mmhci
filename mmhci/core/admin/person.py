from django.contrib import admin

from mmhci.core.models.person import person_address
from mmhci.core.models.person import person_availability
from mmhci.core.models.person import person

admin.site.register(person_address)
admin.site.register(person_availability)
admin.site.register(person)

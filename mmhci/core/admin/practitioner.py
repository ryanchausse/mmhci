from django.contrib import admin

from mmhci.core.models.practitioner import practitioner_address
from mmhci.core.models.practitioner import practitioner_organisation
from mmhci.core.models.practitioner import practitioner

admin.site.register(practitioner_address)
admin.site.register(practitioner_organisation)
admin.site.register(practitioner)

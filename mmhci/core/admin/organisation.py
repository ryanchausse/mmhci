from django.contrib import admin

from mmhci.core.models.organisation import *

admin.site.register(OrganisationAddress)
admin.site.register(OrganisationFormTemplate)
admin.site.register(OrganisationPolicy)
admin.site.register(OrganisationRolePolicy)
admin.site.register(OrganisationUserRole)
admin.site.register(Organisation)

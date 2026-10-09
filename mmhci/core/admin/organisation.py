from django.contrib import admin

from mmhci.core.models.organisation import *

admin.site.register(OrganisationAddress)
admin.site.register(OrganisationFormTemplate)
admin.site.register(OrganisationGroup)
admin.site.register(OrganisationRole)
admin.site.register(OrganisationGroupMembership)

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)

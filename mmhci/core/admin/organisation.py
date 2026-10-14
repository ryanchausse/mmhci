from django.contrib import admin

from mmhci.core.models.organisation import *

admin.site.register(OrganisationAddress)
admin.site.register(OrganisationFormTemplate)


# TODO: create base Admin class to show uuid, created_at, created_by,
# updated_at, and updated_by if present. Also, there is a bug if the UUID
# is present in readonly_fields: when creating a new instance, a UUID is shown
# on the admin "Add" form, but the assigned UUID happens at create time (which
# assigns a new, random UUID)
@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "uuid", "created_at", "created_by", "updated_at", "updated_by"
    )


@admin.register(OrganisationGroup)
class OrganisationGroupAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at", "created_by", "updated_at", "updated_by"
    )


@admin.register(OrganisationRole)
class OrganisationRoleAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at", "created_by", "updated_at", "updated_by"
    )


@admin.register(OrganisationGroupMembership)
class OrganisationGroupMembershipAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at", "created_by", "updated_at", "updated_by"
    )

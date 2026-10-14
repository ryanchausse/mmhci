from mmhci.core.models.organisation import OrganisationRole


class ListOrganisationRolesService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions, prefetch_related for Permissions
        organisation_roles = OrganisationRole.objects.all()
        return organisation_roles

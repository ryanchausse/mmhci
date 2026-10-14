from mmhci.core.models.organisation import OrganisationGroup

class ListOrganisationGroupsService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions, prefetch_related for roles
        organisation_groups = OrganisationGroup.objects.all()
        return organisation_groups

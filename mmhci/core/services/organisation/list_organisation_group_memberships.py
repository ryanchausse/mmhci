from mmhci.core.models.organisation import OrganisationGroupMembership


class ListOrganisationGroupMembershipsService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions, prefetch_related for users/org groups
        organisation_group_memberships = OrganisationGroupMembership.objects.all()
        return organisation_group_memberships

from mmhci.core.models.organisation import Organisation


class ListOrganisationsService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions
        organisations = Organisation.objects.all()
        return organisations

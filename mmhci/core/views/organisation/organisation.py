from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render  # noqa: F401
from django.views.generic import UpdateView
from mmhci.core.models.organisation.organisation import Organisation


def index(request):
    return HttpResponse("Organisation view")


class UpdateOrganisationView(UpdateView):
    model = Organisation
    template_name = "adminlte_4_1/index3.html"
    fields = ['name']

    def get_object(self):
        org_id = self.kwargs.get('org_id')

        # Get the org instance and send the pk
        return get_object_or_404(Organisation, pk=org_id)

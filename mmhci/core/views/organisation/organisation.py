from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render  # noqa: F401
from django.views.generic import UpdateView
# TODO: change interface. This should be a service interface, not a model.
# It's also possible that the service should handle the permissions aspect
from mmhci.core.models.organisation.organisation import Organisation
from mmhci.core.utilities.mixins.org_permission_required import OrgPermissionRequiredMixin


def index(request):
    return HttpResponse("Organisation view")


class UpdateOrganisationView(OrgPermissionRequiredMixin, UpdateView):
    model = Organisation
    template_name = "adminlte_4_1/index3.html"
    fields = ['name']

    # Secure the view using the permission codename instead of a role name
    required_permissions = "change_organisation"

    def get_object(self):
        org_id = self.kwargs.get('org_id')

        # Get the org instance and send the pk
        return get_object_or_404(Organisation, pk=org_id)

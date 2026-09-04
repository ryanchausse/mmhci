from django.views.generic import TemplateView
from mmhci.core.services.person.list_people import ListPeopleService
#from mmhci.core.utilities.mixins.org_permission_required import OrgPermissionRequiredMixin

class ListPeopleView(TemplateView):
    template_name = "adminlte_4_1/mmhci/people/people.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people"] = ListPeopleService().execute()

        return context

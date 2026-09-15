from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.person.list_people import ListPeopleService
#from mmhci.core.utilities.mixins.org_permission_required import OrgPermissionRequiredMixin

class ListPeopleView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/people/people.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_menu"] = True
        context["people_list"] = True
        context["people"] = ListPeopleService(request=self.request).execute()

        return context

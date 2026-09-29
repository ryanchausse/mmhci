from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.person.list_people import ListPeopleService

class ListPeopleView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/people/people.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_menu"] = True
        context["people_list"] = True
        # TODO: send self.request.org_perms as a dict to the service
        # once the service is updated with the permissions service base class
        context["people"] = ListPeopleService(request=self.request).execute()

        return context

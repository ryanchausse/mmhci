from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.organisation.list_organisations import ListOrganisationsService

class ListOrganisationsView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/organisations/organisations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisations_menu"] = True
        context["organisations_list"] = True
        # Can add a .values("name", "description", ...) to restrict fields
        context["organisations"] = ListOrganisationsService(
            request=self.request
        ).execute()

        return context

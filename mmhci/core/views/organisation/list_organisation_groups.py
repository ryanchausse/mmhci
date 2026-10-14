from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.organisation.list_organisation_groups import ListOrganisationGroupsService

class ListOrganisationGroupsView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/organisation_groups/organisation_groups.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_groups_menu"] = True
        context["organisation_groups_list"] = True
        # Can add a .values("name", "description", ...) to restrict fields
        context["organisation_groups"] = ListOrganisationGroupsService(
            request=self.request
        ).execute()

        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.organisation.list_organisation_roles import ListOrganisationRolesService

class ListOrganisationRolesView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/organisation_roles/organisation_roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_roles_menu"] = True
        context["organisation_roles_list"] = True
        # Can add a .values("name", "description", ...) to restrict fields
        context["organisation_roles"] = ListOrganisationRolesService(
            request=self.request
        ).execute()

        return context

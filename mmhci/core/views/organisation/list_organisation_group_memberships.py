from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.organisation.list_organisation_group_memberships import ListOrganisationGroupMembershipsService


class ListOrganisationGroupMembershipsView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/organisation_group_memberships/organisation_group_memberships.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_group_memberships_menu"] = True
        context["organisation_group_memberships_list"] = True
        context["organisation_group_memberships"] = ListOrganisationGroupMembershipsService(
            request=self.request
        ).execute()

        return context

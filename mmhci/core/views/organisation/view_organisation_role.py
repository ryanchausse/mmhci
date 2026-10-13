from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation_role import OrganisationRoleForm
from mmhci.core.services.organisation.view_organisation_role import ViewOrganisationRoleService


class ViewOrganisationRoleView(LoginRequiredMixin, FormView):
    form_class = OrganisationRoleForm
    template_name = "adminlte_4_1/mmhci/organisation_roles/organisation_role_view_or_update.html"
    success_url = reverse_lazy("core:organisation_roles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_roles_menu"] = True

        if self.kwargs.get('pk'):
            organisation_role = ViewOrganisationRoleService(
                request=self.request,
                pk=self.kwargs.get('pk')
            ).execute()
            organisation_role_dict = model_to_dict(organisation_role)
            form = OrganisationRoleForm(initial=organisation_role_dict)
            context["pk"] = organisation_role.pk
            context["form"] = form
        return context

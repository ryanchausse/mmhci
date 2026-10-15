from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation import OrganisationForm
from mmhci.core.services.organisation.view_organisation import ViewOrganisationService


class ViewOrganisationView(LoginRequiredMixin, FormView):
    form_class = OrganisationForm
    template_name = "adminlte_4_1/mmhci/organisations/organisation_view_or_update.html"
    success_url = reverse_lazy("core:organisations:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisations_menu"] = True

        if self.kwargs.get('uuid'):
            organisation = ViewOrganisationService(
                request=self.request,
                uuid=self.kwargs.get('uuid')
            ).execute()
            organisation_dict = model_to_dict(organisation)
            form = OrganisationForm(initial=organisation_dict)
            context["form"] = form
            context["uuid"] = organisation.uuid
        return context

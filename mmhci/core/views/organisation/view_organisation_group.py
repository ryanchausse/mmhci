from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation_group import OrganisationGroupForm
from mmhci.core.services.organisation.view_organisation_group import ViewOrganisationGroupService


class ViewOrganisationGroupView(LoginRequiredMixin, FormView):
    form_class = OrganisationGroupForm
    template_name = "adminlte_4_1/mmhci/organisation_groups/organisation_group_view_or_update.html"
    success_url = reverse_lazy("core:organisation_groups:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_groups_menu"] = True

        if self.kwargs.get('pk'):
            organisation_group = ViewOrganisationGroupService(
                request=self.request,
                pk=self.kwargs.get('pk')
            ).execute()
            organisation_group_dict = model_to_dict(organisation_group)
            # TODO: perhaps with JS, filter roles by org choice in template
            # with htmx trigger on org selection
            organisation_group_dict["organisation_roles"] = list(
                organisation_group.roles.all().values_list('pk', flat=True)
            )
            form = OrganisationGroupForm(initial=organisation_group_dict)
            context["pk"] = organisation_group.pk
            context["form"] = form
        return context

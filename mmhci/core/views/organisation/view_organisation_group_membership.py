from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation_group_membership import OrganisationGroupMembershipForm
from mmhci.core.services.organisation.view_organisation_group_membership import ViewOrganisationGroupMembershipService


class ViewOrganisationGroupMembershipView(LoginRequiredMixin, FormView):
    form_class = OrganisationGroupMembershipForm
    template_name = "adminlte_4_1/mmhci/organisation_group_memberships/organisation_group_membership_view_or_update.html"
    success_url = reverse_lazy("core:organisation_group_memberships:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_group_memberships_menu"] = True

        if self.kwargs.get('pk'):
            organisation_group_membership = ViewOrganisationGroupMembershipService(
                request=self.request,
                pk=self.kwargs.get('pk')
            ).execute()
            organisation_group_membership_dict = model_to_dict(organisation_group_membership)
            form = OrganisationGroupMembershipForm(initial=organisation_group_membership_dict)
            context["pk"] = organisation_group_membership.pk
            context["form"] = form
        return context

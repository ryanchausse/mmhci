from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation_group_membership import OrganisationGroupMembershipForm
from mmhci.core.services.organisation.update_organisation_group_membership import UpdateOrganisationGroupMembershipService


class UpdateOrganisationGroupMembershipView(LoginRequiredMixin, FormView):
    form_class = OrganisationGroupMembershipForm
    template_name = "adminlte_4_1/mmhci/organisation_group_memberships/organisation_group_membership_view_or_update_form_htmx.html"
    success_url = reverse_lazy("core:organisation_group_membership:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_group_membership_menu"] = True
        return context

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        organisation_group_membership = UpdateOrganisationGroupMembershipService(
            request=self.request,
            pk=pk,
            data=dict(form.cleaned_data)
        ).execute()
        messages.success(
            self.request,
            f'Membership updated successfully'
        )
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisation_group_memberships/partial/organisation_group_membership_view_or_update_form_htmx.html',
                {'pk': pk, 'form': form},
                status=200
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            pk = self.kwargs.get('pk')
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisation_group_memberships/partial/organisation_group_membership_view_or_update_form_htmx.html',
                {'pk': pk, 'form': form},
                status=422
            )
        return super().form_invalid(form)

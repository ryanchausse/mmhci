from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation_group_membership import OrganisationGroupMembershipForm
from mmhci.core.services.organisation.create_organisation_group_membership import CreateOrganisationGroupMembershipService


class CreateOrganisationGroupMembershipFormView(LoginRequiredMixin, FormView):
    form_class = OrganisationGroupMembershipForm
    template_name = 'adminlte_4_1/mmhci/organisation_group_memberships/organisation_group_membership_create.html'
    success_url = reverse_lazy("core:organisation_group_memberships:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_group_memberships_menu"] = True
        context["organisation_group_membership_create"] = True
        return context

    def form_valid(self, form):
        organisation_group_membership = CreateOrganisationGroupMembershipService(
            request=self.request,
            data=form.cleaned_data
        ).execute()
        messages.success(
            self.request,
            f'Membership created successfully'
        )
        url = reverse_lazy(
            'core:organisation_group_memberships:view',
            kwargs={
                'pk': organisation_group_membership.pk
            }
        )
        return redirect(url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisation_group_memberships/partial/organisation_group_membership_create_form.html',
                {'form': form},
                status=422
            )
        return super().form_invalid(form)

def index(request):
    return HttpResponse("Create Organisation Group Membership view")

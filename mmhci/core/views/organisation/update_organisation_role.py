from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation_role import OrganisationRoleForm
from mmhci.core.services.organisation.update_organisation_role import UpdateOrganisationRoleService


class UpdateOrganisationRoleView(LoginRequiredMixin, FormView):
    form_class = OrganisationRoleForm
    template_name = "adminlte_4_1/mmhci/organisation_roles/organisation_role_view_or_update_form_htmx.html"
    success_url = reverse_lazy("core:organisation_role:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_role_menu"] = True
        return context

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        organisation_role = UpdateOrganisationRoleService(
            request=self.request,
            pk=pk,
            data=dict(form.cleaned_data)
        ).execute()
        messages.success(
            self.request,
            f'{organisation_role.name} updated successfully'
        )
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisation_roles/partial/organisation_role_view_or_update_form_htmx.html',
                {'pk': pk, 'form': form},
                status=200
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            pk = self.kwargs.get('pk')
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisation_roles/partial/organisation_role_view_or_update_form_htmx.html',
                {'pk': pk, 'form': form},
                status=422
            )
        return super().form_invalid(form)

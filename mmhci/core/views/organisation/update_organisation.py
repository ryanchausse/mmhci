from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation import OrganisationForm
from mmhci.core.services.organisation.update_organisation import UpdateOrganisationService


class UpdateOrganisationView(LoginRequiredMixin, FormView):
    form_class = OrganisationForm
    template_name = "adminlte_4_1/mmhci/organisations/organisation_view_or_update_form_htmx.html"
    success_url = reverse_lazy("core:organisation:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation_menu"] = True
        return context

    def form_valid(self, form):
        uuid = self.kwargs.get('uuid')
        organisation = UpdateOrganisationService(
            request=self.request,
            uuid=uuid,
            data=dict(form.cleaned_data)
        ).execute()
        messages.success(
            self.request,
            f'{organisation.name} updated successfully'
        )
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisations/partial/organisation_view_or_update_form_htmx.html',
                {'uuid': uuid, 'form': form},
                status=200
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            uuid = self.kwargs.get('uuid')
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisations/partial/organisation_view_or_update_form_htmx.html',
                {'uuid': uuid, 'form': form},
                status=422
            )
        return super().form_invalid(form)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation import OrganisationForm
from mmhci.core.services.organisation.create_organisation import CreateOrganisationService


class CreateOrganisationFormView(LoginRequiredMixin, FormView):
    # Views are responsible for validation of input, invoking services, and page flow
    form_class = OrganisationForm
    template_name = 'adminlte_4_1/mmhci/organisations/organisation_create.html'
    success_url = reverse_lazy("core:organisations:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisations_menu"] = True
        context["organisation_create"] = True
        return context

    def form_valid(self, form):
        organisation = CreateOrganisationService(
            request=self.request,
            data=form.cleaned_data
        ).execute()
        messages.success(
            self.request,
            f'{organisation.name} created successfully'
        )
        url = reverse_lazy(
            'core:organisations:view',
            kwargs={
                'uuid': organisation.uuid
            }
        )
        return redirect(url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisations/partial/organisation_create_form.html',
                {'form': form},
                status=422
            )
        return super().form_invalid(form)

def index(request):
    return HttpResponse("Create Organisation view")

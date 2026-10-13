from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.organisation.organisation_role import OrganisationRoleForm
from mmhci.core.services.organisation.create_organisation_role import CreateOrganisationRoleService


class CreateOrganisationRoleFormView(LoginRequiredMixin, FormView):
    # Views are responsible for validation of input, invoking services, and page flow
    form_class = OrganisationRoleForm
    template_name = 'adminlte_4_1/mmhci/organisation_roles/organisation_role_create.html'
    success_url = reverse_lazy("core:organisation_roles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["organisation_roles_menu"] = True
        context["organisation_role_create"] = True
        return context

    def form_valid(self, form):
        organisation_role = CreateOrganisationRoleService(
            request=self.request,
            data=form.cleaned_data
        ).execute()
        messages.success(
            self.request,
            f'{organisation_role.name} created successfully'
        )
        url = reverse_lazy(
            'core:organisation_roles:view',
            kwargs={
                'pk': organisation_role.pk
            }
        )
        return redirect(url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/organisation_roles/partial/organisation_role_create_form.html',
                {'form': form},
                status=422
            )
        return super().form_invalid(form)

def index(request):
    return HttpResponse("Create Organisation Role view")

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.update_person import UpdatePersonService


class UpdatePersonView(LoginRequiredMixin, FormView):
    form_class = PersonForm
    template_name = "adminlte_4_1/mmhci/people/person_view_or_update_form_htmx.html"
    success_url = reverse_lazy("core:people:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_menu"] = True
        return context

    def form_valid(self, form):
        uuid = self.kwargs.get('uuid')
        person = UpdatePersonService(
            request=self.request,
            uuid=uuid,
            data=dict(form.cleaned_data)
        ).execute()
        messages.success(
            self.request,
            f'{person.first_name} {person.last_name} updated successfully'
        )
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_view_or_update_form_htmx.html',
                {'uuid': uuid, 'form': form},
                status=200
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            uuid = self.kwargs.get('uuid')
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_view_or_update_form_htmx.html',
                {'uuid': uuid, 'form': form},
                status=422
            )
        return super().form_invalid(form)

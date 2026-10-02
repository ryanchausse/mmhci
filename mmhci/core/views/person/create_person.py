from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.create_person import CreatePersonService


class CreatePersonFormView(LoginRequiredMixin, FormView):
    # Views are responsible for validation of input, invoking services, and page flow
    form_class = PersonForm
    template_name = 'adminlte_4_1/mmhci/people/person_create.html'
    success_url = reverse_lazy("core:people:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_menu"] = True
        context["person_create"] = True
        return context

    def form_valid(self, form):
        person = CreatePersonService(**form.cleaned_data).execute()
        messages.success(
            self.request,
            f'{person.first_name} {person.last_name} created successfully'
        )
        url = reverse_lazy(
            'core:people:view_or_update',
            kwargs={
                'uuid': person.uuid
            }
        )
        return redirect(url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_create_form.html',
                {'form': form},
                status=422
            )
        return super().form_invalid(form)

def index(request):
    return HttpResponse("Create Person view")

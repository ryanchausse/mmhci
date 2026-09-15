from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.create_person import CreatePersonService


class CreatePersonFormView(LoginRequiredMixin, FormView):
    # Views are responsible for validation of input, invoking services, and page flow
    form_class = PersonForm
    template_name = 'adminlte_4_1/mmhci/people/person_create.html'
    # Probably insert a flash message or something instead of redirect to root
    success_url = reverse_lazy("core:people:create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_menu"] = True
        context["person_create"] = True
        return context

    def form_valid(self, form):
        print('Form data validated.')
        if self.request.htmx:
            # NB: need to save fields manually because PersonForm inherits from
            # forms.Form, not forms.ModelForm
            person = CreatePersonService(**form.cleaned_data).execute()
            create_person_success_message = f'Person ID = {person.id}'
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_create_success.html',
                {'create_person_success_message': create_person_success_message},
                status=201
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form data is not valid.')
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

from django.http import HttpResponse
from django.shortcuts import render  # noqa: F401
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.create_person import CreatePersonService


class PersonFormView(FormView):
    # Views are responsible for validation of input, invoking services, and page flow
    form_class = PersonForm
    template_name = 'adminlte_4_1/mmhci/people/person_create.html'
    # Probably insert a flash message or something instead of redirect to root
    success_url = '/'

    def form_valid(self, form):
        print('Form data validated.')
        if self.request.htmx:
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
    return HttpResponse("Person view")

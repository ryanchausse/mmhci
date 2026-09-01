from django.http import HttpResponse
from django.shortcuts import render  # noqa: F401
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm


class PersonFormView(FormView):
    form_class = PersonForm
    template_name = 'adminlte_4_1/mmhci/people/person_create.html'
    # Probably insert a flash message or something instead of redirect to root
    success_url = '/'

    def form_valid(self, form):
        print('Form data validated.')
        if self.request.htmx:
            return HttpResponse('<div>Form data is valid.</div>')
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form data is not valid.')
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_create_form_container.html',
                {'form': form},
                status=200
            )
        return super().form_invalid(form)

def index(request):
    return HttpResponse("Person view")

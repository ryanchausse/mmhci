from django.http import HttpResponse
from django.shortcuts import render  # noqa: F401
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm


class PersonFormView(FormView):
    form_class = PersonForm
    template_name = ''


    def form_valid(self, form):
        print('Form data validated.')
        if self.request.htmx:
            return HttpResponse('<div>Form data is valid.</div>')
        raise NotImplemented

    def form_invalid(self, form):
        if self.request.htmx:
            return HttpResponse('Form data is not valid.</div>')
        raise NotImplemented

def index(request):
    return HttpResponse("Person view")

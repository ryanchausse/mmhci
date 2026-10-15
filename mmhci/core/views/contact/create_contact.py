from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.contact.contact import ContactForm
from mmhci.core.services.contact.create_contact import CreateContactService


class CreateContactFormView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = 'adminlte_4_1/mmhci/contacts/contact_create.html'
    success_url = reverse_lazy("core:contacts:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts_menu"] = True
        context["contact_create"] = True
        return context

    def form_valid(self, form):
        contact = CreateContactService(
            request=self.request,
            data=form.cleaned_data
        ).execute()
        messages.success(
            self.request,
            f'Contact created successfully'
        )
        url = reverse_lazy(
            'core:contacts:view',
            kwargs={
                'uuid': contact.uuid
            }
        )
        return redirect(url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/contacts/partial/contact_create_form.html',
                {'form': form},
                status=422
            )
        return super().form_invalid(form)

def index(request):
    return HttpResponse("Create Contact view")

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.contact.contact import ContactForm
from mmhci.core.services.contact.view_contact import ViewContactService


class ViewContactView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = "adminlte_4_1/mmhci/contacts/contact_view_or_update.html"
    success_url = reverse_lazy("core:contacts:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts_menu"] = True

        if self.kwargs.get('uuid'):
            contact = ViewContactService(
                request=self.request,
                uuid=self.kwargs.get('uuid')
            ).execute()
            contact_dict = model_to_dict(contact)
            form = ContactForm(initial=contact_dict)
            context["form"] = form
            context["uuid"] = contact.uuid
        return context

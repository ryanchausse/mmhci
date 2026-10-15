from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.contact.list_contacts import ListContactsService


class ListContactsView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/contacts/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts_menu"] = True
        context["contacts_list"] = True
        context["contacts"] = ListContactsService(request=self.request).execute()

        return context

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.view_person import ViewPersonService


class ViewPersonView(LoginRequiredMixin, FormView):
    form_class = PersonForm
    template_name = "adminlte_4_1/mmhci/people/person_view_or_update.html"
    success_url = reverse_lazy("core:people:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # # Get permissions for request.user (refreshed on every request, unchanging)
        # self.logger.info("Org permission data: %s", self.request.org_perms)
        # # Get the current org id for request.user. Can also set the session variable.
        # self.logger.info("Current org: %s", self.request.session["current_org_id"])
        context["people_menu"] = True

        if self.kwargs.get('uuid'):
            person = ViewPersonService(
                request=self.request,
                uuid=self.kwargs.get('uuid')
            ).execute()
            person_dict = model_to_dict(person)
            form = PersonForm(initial=person_dict)
            context["form"] = form
            context["uuid"] = person.uuid
        return context

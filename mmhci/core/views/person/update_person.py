# import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.update_person import UpdatePersonService


class UpdatePersonView(LoginRequiredMixin, FormView):
    # logger = logging.getLogger(__name__)
    form_class = PersonForm
    template_name = "adminlte_4_1/mmhci/people/person_view_or_update_form_htmx.html"
    success_url = reverse_lazy("core:people:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # # Get permissions for request.user (refreshed on every request, unchanging)
        # self.logger.info("Org permission data: %s", self.request.org_perms)
        # # Get the current org id for request.user. Can also set the session variable.
        # self.logger.info("Current org: %s", self.request.session["current_org_id"])
        context["people_menu"] = True
        return context

    def form_valid(self, form):
        self.logger.info("form valid")
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
        self.logger.info("form invalid")
        # self.logger.info("Org permission data: %s", self.request.org_perms)
        if self.request.htmx:
            uuid = self.kwargs.get('uuid')
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_view_or_update_form_htmx.html',
                {'uuid': uuid, 'form': form},
                status=422
            )
        return super().form_invalid(form)

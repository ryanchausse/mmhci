from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.view_or_update_person import ViewOrUpdatePersonService
#from mmhci.core.utilities.mixins.org_permission_required import OrgPermissionRequiredMixin

class ViewOrUpdatePersonView(LoginRequiredMixin, FormView):
    form_class = PersonForm
    template_name = "adminlte_4_1/mmhci/people/person_view_or_update.html"
    success_url = reverse_lazy("core:people:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_menu"] = True
        if self.kwargs.get('pk'):
            person = ViewOrUpdatePersonService(
                request=self.request,
                pk=self.kwargs.get('pk')
            ).execute()
            person_dict = model_to_dict(person)
            form = PersonForm(initial=person_dict)
            context["form"] = form
            context["pk"] = person_dict.get('id')
        return context

    def form_valid(self, form):
        print('Form data validated.')
        pk = self.kwargs.get('pk')
        # NB: need to save fields manually because PersonForm inherits from
        # forms.Form, not forms.ModelForm.
        # TODO: separate view from update?
        person = ViewOrUpdatePersonService(
            request=self.request,
            pk=pk,
            form=form,
            update=True
        ).execute()
        messages.success(self.request, f'{person.first_name} {person.last_name} updated successfully')
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_view_or_update_form_htmx.html',
                {'pk': pk, 'form': form},
                status=200
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form data is not valid.')
        if self.request.htmx:
            pk = self.kwargs.get('pk')
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_view_or_update_form_htmx.html',
                {'pk': pk, 'form': form},
                status=422
            )
        return super().form_invalid(form)

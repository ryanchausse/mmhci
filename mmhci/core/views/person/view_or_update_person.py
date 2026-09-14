from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import FormView

from mmhci.core.forms.person.person import PersonForm
from mmhci.core.services.person.view_or_update_person import ViewOrUpdatePersonService
#from mmhci.core.utilities.mixins.org_permission_required import OrgPermissionRequiredMixin

class ViewOrUpdatePersonView(LoginRequiredMixin, FormView):
    form_class = PersonForm
    template_name = "adminlte_4_1/mmhci/people/person_view_or_update.html"
    # Probably insert a flash message or something instead of redirect to root
    success_url = '/'

    def get_initial(self):
        if self.request.method == 'GET':
            if not self.kwargs.get('pk'):
                return super().get_initial()
            initial_with_person = super().get_initial()
            person_id = self.kwargs.get('pk')
            person = ViewOrUpdatePersonService(
                request=self.request,
                pk=person_id
            ).execute()
            initial_with_person.update(model_to_dict(person))
            return initial_with_person

    def form_valid(self, form):
        print('Form data validated.')
        pk = self.kwargs.get('pk')
        # NB: need to save fields manually because PersonForm inherits from
        # forms.Form, not forms.ModelForm
        # TODO: probably separate view from update, but the htmx form partial has two
        # if conditions - one to evaluate whether the var "pk" is present, and one to
        # see if the form has returned a "form.initial.id".
        person = ViewOrUpdatePersonService(
            request=self.request,
            pk=pk,
            form=form,
            update=True
        ).execute()
        messages.success(self.request, f'{person.first_name} {person.last_name} updated successfully')
        if self.request.htmx:
            # Might want to render just the replacement template partial.
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_view_or_update_form_htmx.html',
                {'pk': pk, 'form': form},
                status=200
            )
            # pass
        # return redirect('core:people:view_or_update', pk=pk)
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form data is not valid.')
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/people/partial/person_view_or_update_form.html',
                {'form': form},
                status=422
            )
        return super().form_invalid(form)

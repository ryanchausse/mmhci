from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.user.user import UserForm
from mmhci.core.services.user.create_user import CreateUserService


class CreateUserFormView(LoginRequiredMixin, FormView):
    # Views are responsible for validation of input, invoking services, and page flow
    form_class = UserForm
    template_name = 'adminlte_4_1/mmhci/admin/users/user_create.html'
    success_url = reverse_lazy("core:users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["users_menu"] = True
        context["user_create"] = True
        return context

    def form_valid(self, form):
        user = CreateUserService(
            request=self.request,
            data=form.cleaned_data
        ).execute()
        messages.success(
            self.request,
            f'{user.email} created successfully'
        )
        url = reverse_lazy(
            'core:users:view',
            kwargs={
                'uuid': user.uuid
            }
        )
        return redirect(url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/admin/users/partial/user_create_form.html',
                {'form': form},
                status=422
            )
        return super().form_invalid(form)

def index(request):
    return HttpResponse("Create User view")

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.user.user import UserForm
from mmhci.core.services.user.view_user import ViewUserService


class ViewUserView(LoginRequiredMixin, FormView):
    form_class = UserForm
    template_name = "adminlte_4_1/mmhci/admin/users/user_view_or_update.html"
    success_url = reverse_lazy("core:users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["users_menu"] = True

        if self.kwargs.get('uuid'):
            user = ViewUserService(
                request=self.request,
                uuid=self.kwargs.get('uuid')
            ).execute()
            user_dict = model_to_dict(user)
            form = UserForm(initial=user_dict)
            for field in form.fields.values():
                field.disabled = True
            context["form"] = form
            context["uuid"] = user.uuid
        return context

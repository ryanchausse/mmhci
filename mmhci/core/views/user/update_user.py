from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mmhci.core.forms.user.user import UserForm
from mmhci.core.services.user.update_user import UpdateUserService


class UpdateUserView(LoginRequiredMixin, FormView):
    form_class = UserForm
    template_name = "adminlte_4_1/mmhci/admin/users/user_view_or_update_form_htmx.html"
    success_url = reverse_lazy("core:users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["users_menu"] = True
        return context

    def form_valid(self, form):
        uuid = self.kwargs.get('uuid')
        user = UpdateUserService(
            request=self.request,
            uuid=uuid,
            data=dict(form.cleaned_data)
        ).execute()
        messages.success(
            self.request,
            f'{user.email} updated successfully'
        )
        if self.request.htmx:
            return render(
                self.request,
                'adminlte_4_1/mmhci/admin/users/partial/user_view_or_update_form_htmx.html',
                {'uuid': uuid, 'form': form},
                status=200
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            uuid = self.kwargs.get('uuid')
            return render(
                self.request,
                'adminlte_4_1/mmhci/admin/users/partial/user_view_or_update_form_htmx.html',
                {'uuid': uuid, 'form': form},
                status=422
            )
        return super().form_invalid(form)

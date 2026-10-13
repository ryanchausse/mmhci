from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.user.list_users import ListUsersService

class ListUsersView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/admin/users/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config_menu"] = True
        context["users_menu"] = True
        context["users_list"] = True
        context["users"] = ListUsersService(request=self.request).execute()

        return context

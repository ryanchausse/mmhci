from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from mmhci.core.services.person.list_people_with_permissions_example import ListPeopleService


class ListPeopleView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/people/people.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_perms = getattr(self.request, "org_perms", {})
        try:
            # TODO: this is the correct usage, but switch it out
            list_people_service = ListPeopleService(org_perms=org_perms)
            context["people"] = list_people_service.execute()
        except PermissionDenied:
            raise PermissionDenied("You do not have access to list people.")

        context["people_menu"] = True
        context["people_list"] = True

        return context

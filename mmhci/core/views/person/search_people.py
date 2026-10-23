from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from mmhci.core.services.person.list_people import ListPeopleService


class SearchPeopleView(LoginRequiredMixin, TemplateView):
    template_name = "adminlte_4_1/mmhci/people/partial/people_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q", "")
        context["people"] = ListPeopleService(
            request=self.request
        ).search(q=q)

        return context

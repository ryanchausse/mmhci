from django.urls import path
from django.views.generic import TemplateView

from mmhci.core.views.person import person

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="adminlte_4_1/mmhci/people/people.html"),
        name="list",
    ),
    path(
        "create",
        person.PersonFormView.as_view(
            template_name="adminlte_4_1/mmhci/people/person_create.html"
        ),
        name="person_create",
    ),
]

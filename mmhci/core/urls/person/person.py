from django.urls import path
from django.views.generic import TemplateView

from mmhci.core.views.person import create_person, list_people

urlpatterns = [
    path(
        "",
        list_people.ListPeopleView.as_view(
            template_name="adminlte_4_1/mmhci/people/list_people.html"
        ),
        name="list",
    ),
    path(
        "create",
        create_person.CreatePersonFormView.as_view(
            template_name="adminlte_4_1/mmhci/people/person_create.html"
        ),
        name="create",
    ),
]

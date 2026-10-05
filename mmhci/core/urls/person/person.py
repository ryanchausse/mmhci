from django.urls import path

from mmhci.core.views.person import create_person
from mmhci.core.views.person import list_people
from mmhci.core.views.person import view_person
from mmhci.core.views.person import update_person

urlpatterns = [
    path(
        "",
        list_people.ListPeopleView.as_view(
            template_name="adminlte_4_1/mmhci/people/list_people.html"
        ),
        name="list",
    ),
    path(
        "<uuid:uuid>/",
        view_person.ViewPersonView.as_view(
            template_name="adminlte_4_1/mmhci/people/person_view_or_update.html"
        ),
        name="view",
    ),
    path(
        "<uuid:uuid>/update",
        update_person.UpdatePersonView.as_view(
            template_name="adminlte_4_1/mmhci/people/person_view_or_update.html"
        ),
        name="update",
    ),
    path(
        "create",
        create_person.CreatePersonFormView.as_view(
            template_name="adminlte_4_1/mmhci/people/person_create.html"
        ),
        name="create",
    ),
]

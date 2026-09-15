from django.urls import path

from mmhci.core.views.person import create_person, list_people, view_or_update_person

urlpatterns = [
    path(
        "",
        list_people.ListPeopleView.as_view(
            template_name="adminlte_4_1/mmhci/people/list_people.html"
        ),
        name="list",
    ),
    path(
        "view/<int:pk>/",
        view_or_update_person.ViewOrUpdatePersonView.as_view(
            template_name="adminlte_4_1/mmhci/people/person_view_or_update.html"
        ),
        name="view_or_update",
    ),
    path(
        "create",
        create_person.CreatePersonFormView.as_view(
            template_name="adminlte_4_1/mmhci/people/person_create.html"
        ),
        name="create",
    ),
]

from django.urls import path

from mmhci.core.views.organisation import list_organisation_groups
from mmhci.core.views.organisation import create_organisation_group
from mmhci.core.views.organisation import view_organisation_group
from mmhci.core.views.organisation import update_organisation_group

urlpatterns = [
    path(
        "",
        list_organisation_groups.ListOrganisationGroupsView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_groups/list_organisation_groups.html"
        ),
        name="list",
    ),
    path(
        "<int:pk>/",
        view_organisation_group.ViewOrganisationGroupView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_groups/organisation_group_view_or_update.html"
        ),
        name="view",
    ),
    path(
        "<int:pk>/update",
        update_organisation_group.UpdateOrganisationGroupView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_groups/organisation_group_view_or_update.html"
        ),
        name="update",
    ),
    path(
        "create",
        create_organisation_group.CreateOrganisationGroupFormView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_groups/organisation_group_create.html"
        ),
        name="create",
    ),
]

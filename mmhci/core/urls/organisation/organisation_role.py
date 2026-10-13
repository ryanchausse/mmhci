from django.urls import path

from mmhci.core.views.organisation import list_organisation_roles
from mmhci.core.views.organisation import create_organisation_role
from mmhci.core.views.organisation import view_organisation_role
from mmhci.core.views.organisation import update_organisation_role

urlpatterns = [
    path(
        "",
        list_organisation_roles.ListOrganisationRolesView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_roles/list_organisation_roles.html"
        ),
        name="list",
    ),
    path(
        "<int:pk>/",
        view_organisation_role.ViewOrganisationRoleView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_roles/organisation_role_view_or_update.html"
        ),
        name="view",
    ),
    path(
        "<int:pk>/update",
        update_organisation_role.UpdateOrganisationRoleView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_roles/organisation_role_view_or_update.html"
        ),
        name="update",
    ),
    path(
        "create",
        create_organisation_role.CreateOrganisationRoleFormView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_roles/organisation_role_create.html"
        ),
        name="create",
    ),
]

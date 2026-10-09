from django.urls import path

from mmhci.core.views.organisation import list_organisations
from mmhci.core.views.organisation import create_organisation
from mmhci.core.views.organisation import view_organisation
from mmhci.core.views.organisation import update_organisation

urlpatterns = [
    path(
        "",
        list_organisations.ListOrganisationsView.as_view(
            template_name="adminlte_4_1/mmhci/organisations/list_organisations.html"
        ),
        name="list",
    ),
    path(
        "<uuid:uuid>/",
        view_organisation.ViewOrganisationView.as_view(
            template_name="adminlte_4_1/mmhci/organisations/organisation_view_or_update.html"
        ),
        name="view",
    ),
    path(
        "<uuid:uuid>/update",
        update_organisation.UpdateOrganisationView.as_view(
            template_name="adminlte_4_1/mmhci/organisations/organisation_view_or_update.html"
        ),
        name="update",
    ),
    path(
        "create",
        create_organisation.CreateOrganisationFormView.as_view(
            template_name="adminlte_4_1/mmhci/organisations/organisation_create.html"
        ),
        name="create",
    ),
]

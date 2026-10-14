from django.urls import path

from mmhci.core.views.organisation import list_organisation_group_memberships
from mmhci.core.views.organisation import create_organisation_group_membership
from mmhci.core.views.organisation import view_organisation_group_membership
from mmhci.core.views.organisation import update_organisation_group_membership

urlpatterns = [
    path(
        "",
        list_organisation_group_memberships.ListOrganisationGroupMembershipsView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_group_memberships/list_organisation_group_memberships.html"
        ),
        name="list",
    ),
    path(
        "<int:pk>/",
        view_organisation_group_membership.ViewOrganisationGroupMembershipView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_group_memberships/organisation_group_membership_view_or_update.html"
        ),
        name="view",
    ),
    path(
        "<int:pk>/update",
        update_organisation_group_membership.UpdateOrganisationGroupMembershipView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_group_memberships/organisation_group_membership_view_or_update.html"
        ),
        name="update",
    ),
    path(
        "create",
        create_organisation_group_membership.CreateOrganisationGroupMembershipFormView.as_view(
            template_name="adminlte_4_1/mmhci/organisation_group_memberships/organisation_group_membership_create.html"
        ),
        name="create",
    ),
]

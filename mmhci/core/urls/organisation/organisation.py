from django.urls import path

from mmhci.core.views.organisation import organisation
from mmhci.core.views.organisation.organisation import UpdateOrganisationView

urlpatterns = [
    path("", organisation.index, name="index"),
    # Just an example for a complete cycle, including permissions mixin
    path("<int:org_id>/update/", UpdateOrganisationView.as_view(), name="update_org")
]

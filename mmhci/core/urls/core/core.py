from django.urls import path

from mmhci.core.views.core import change_current_org

urlpatterns = [
    path(
        "change_current_org",
        change_current_org.ChangeCurrentOrgView.as_view(),
        name="change_current_org",
    ),
]

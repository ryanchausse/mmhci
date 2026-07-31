from django.urls import path

from mmhci.core.views.role import role

urlpatterns = [
    path("", role.index, name="index"),
]

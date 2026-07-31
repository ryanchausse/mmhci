from django.urls import path

from mmhci.core.views.organisation import organisation

urlpatterns = [
    path("", organisation.index, name="index"),
]

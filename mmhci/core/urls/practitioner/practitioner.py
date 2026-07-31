from django.urls import path

from mmhci.core.views.practitioner import practitioner

urlpatterns = [
    path("", practitioner.index, name="index"),
]

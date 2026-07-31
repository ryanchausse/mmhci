from django.urls import path

from mmhci.core.views.consent import consent

urlpatterns = [
    path("", consent.index, name="index"),
]

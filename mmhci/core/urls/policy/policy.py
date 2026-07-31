from django.urls import path

from mmhci.core.views.policy import policy

urlpatterns = [
    path("", policy.index, name="index"),
]

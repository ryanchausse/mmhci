from django.urls import path

from mmhci.core.views.assessment import assessment

urlpatterns = [
    path("", assessment.index, name="index"),
]

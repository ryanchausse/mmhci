from django.urls import path

from mmhci.core.views.survey import survey

urlpatterns = [
    path("", survey.index, name="index"),
]

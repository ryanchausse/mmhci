from django.urls import path

from mmhci.core.views.log import log

urlpatterns = [
    path("", log.index, name="index"),
]

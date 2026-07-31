from django.urls import path

from mmhci.core.views.tag import tag

urlpatterns = [
    path("", tag.index, name="index"),
]

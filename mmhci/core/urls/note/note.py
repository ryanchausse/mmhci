from django.urls import path

from mmhci.core.views.note import note

urlpatterns = [
    path("", note.index, name="index"),
]

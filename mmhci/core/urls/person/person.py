from django.urls import path

from mmhci.core.views.person import person

urlpatterns = [
    path("", person.index, name="index"),
]

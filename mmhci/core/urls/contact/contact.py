from django.urls import path

from mmhci.core.views.contact import contact

urlpatterns = [
    path("", contact.index, name="index"),
]

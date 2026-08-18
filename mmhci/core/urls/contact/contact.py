from django.urls import path
from django.views.generic import TemplateView

from mmhci.core.views.contact import contact

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="adminlte_4_1/mmhci/contacts/contacts.html"),
        name="list",
    ),
    path("test", contact.index, name="index"),
]

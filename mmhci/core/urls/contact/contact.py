from django.urls import path

from mmhci.core.views.contact import create_contact
from mmhci.core.views.contact import list_contacts
from mmhci.core.views.contact import view_contact
from mmhci.core.views.contact import update_contact

urlpatterns = [
    path(
        "",
        list_contacts.ListContactsView.as_view(
            template_name="adminlte_4_1/mmhci/contacts/list_contacts.html"
        ),
        name="list",
    ),
    path(
        "<uuid:uuid>/",
        view_contact.ViewContactView.as_view(
            template_name="adminlte_4_1/mmhci/contacts/contact_view_or_update.html"
        ),
        name="view",
    ),
    path(
        "<uuid:uuid>/update",
        update_contact.UpdateContactView.as_view(
            template_name="adminlte_4_1/mmhci/contacts/contact_view_or_update.html"
        ),
        name="update",
    ),
    path(
        "create",
        create_contact.CreateContactFormView.as_view(
            template_name="adminlte_4_1/mmhci/contacts/contact_create.html"
        ),
        name="create",
    ),
]

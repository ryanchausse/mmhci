from mmhci.core.models.contact import Contact


class ListContactsService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: permissions as in ListUsersService
        contacts = Contact.objects.all()
        return contacts

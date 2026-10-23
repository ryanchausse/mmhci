from mmhci.core.models.person import Person


class ListPeopleService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions; send private or full name depending
        # see the Person model for custom properties for name/permissions
        people = Person.objects.all()
        return people

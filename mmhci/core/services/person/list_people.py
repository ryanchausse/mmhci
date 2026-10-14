from mmhci.core.models.person import Person


class ListPeopleService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions
        people = Person.objects.all()
        return people

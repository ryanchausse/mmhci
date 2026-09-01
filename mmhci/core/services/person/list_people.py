from mmhci.core.models.person import Person

class ListPeopleService:

    def execute(self):
        # TODO: enforce permissions (define with a string first, then check)
        people = Person.objects.all()
        return people

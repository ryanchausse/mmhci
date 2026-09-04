from mmhci.core.models.person import Person

class ListPeopleService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions (set permission name as a string)
        # Possibly need to place permission logic here instead of in the Views/API
        # routers so permissions are enforced no matter where the call comes from.
        # Maybe create a service base class that does this? In the current plan, we
        # would need the user and the org_id (org context)
        people = Person.objects.all()
        return people

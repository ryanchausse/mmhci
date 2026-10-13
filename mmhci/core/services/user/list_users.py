from mmhci.users.models import User

class ListUsersService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        # TODO: enforce permissions
        users = User.objects.all()
        return users

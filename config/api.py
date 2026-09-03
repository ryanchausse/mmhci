from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja.security import SessionAuth

api = NinjaAPI(
    urls_namespace="api",
    auth=SessionAuth(),
    docs_decorator=staff_member_required,
)

api.add_router("/users/", "mmhci.users.api.views.router")

@api.get("/ping")
def ping(request):
    return {"success": True}

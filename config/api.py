from django.contrib.admin.views.decorators import staff_member_required
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja_extra.throttling import AnonRateThrottle, UserRateThrottle
from ninja_jwt.authentication import JWTAuth

api = NinjaExtraAPI(
    urls_namespace="api",
    auth=JWTAuth(),
    docs_decorator=staff_member_required,
    throttle=[
        AnonRateThrottle(),
        UserRateThrottle()
    ]
)

api.register_controllers(NinjaJWTDefaultController)
api.add_router("/users/", "mmhci.users.api.views.router")

# Routes are protected by default, can override auth like so:
@api.get("/ping", auth=None)
def ping(request):
    return {"success": True}

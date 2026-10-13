from ninja import Router

user_router = Router()

@user_router.get("")
def list_uploads(request):
    return {"users": ["Sample collection item"]}

@user_router.get("/test")
def test_path(request):
    return {"test": "success"}

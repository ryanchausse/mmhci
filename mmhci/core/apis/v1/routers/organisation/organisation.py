from ninja import Router

organisation_router = Router()

@organisation_router.get("")
def list_organisations(request):
    return {"organisations": ["Sample collection item"]}

@organisation_router.get("/test")
def test_path(request):
    return {"test": "success"}

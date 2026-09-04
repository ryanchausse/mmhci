from ninja import Router

contact_router = Router()

@contact_router.get("")
def list_contacts(request):
    return {"contacts": ["Sample collection item"]}

@contact_router.get("/test")
def test_path(request):
    return {"test": "success"}

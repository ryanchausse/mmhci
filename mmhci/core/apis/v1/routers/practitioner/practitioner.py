from ninja import Router

practitioner_router = Router()

@practitioner_router.get("")
def list_practitioners(request):
    return {"practitioners": ["Sample collection item"]}

@practitioner_router.get("/test")
def test_path(request):
    return {"test": "success"}

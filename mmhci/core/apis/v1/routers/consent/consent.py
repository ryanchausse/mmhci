from ninja import Router

consent_router = Router()

@consent_router.get("")
def list_consents(request):
    return {"consents": ["Sample collection item"]}

@consent_router.get("/test")
def test_path(request):
    return {"test": "success"}

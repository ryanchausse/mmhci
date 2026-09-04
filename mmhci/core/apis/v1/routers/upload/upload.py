from ninja import Router

upload_router = Router()

@upload_router.get("")
def list_uploads(request):
    return {"uploads": ["Sample collection item"]}

@upload_router.get("/test")
def test_path(request):
    return {"test": "success"}

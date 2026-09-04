from ninja import Router

tag_router = Router()

@tag_router.get("")
def list_tags(request):
    return {"tags": ["Sample collection item"]}

@tag_router.get("/test")
def test_path(request):
    return {"test": "success"}

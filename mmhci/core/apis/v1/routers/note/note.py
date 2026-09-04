from ninja import Router

note_router = Router()

@note_router.get("")
def list_notes(request):
    return {"notes": ["Sample collection item"]}

@note_router.get("/test")
def test_path(request):
    return {"test": "success"}

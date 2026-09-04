from ninja import Router

person_router = Router()

@person_router.get("/")
def list_people(request):
    return {"people": ["Rev. Dr. Martin Luther King Jr."]}

@person_router.get("test")
def test_path(request):
    return {"test": "success"}

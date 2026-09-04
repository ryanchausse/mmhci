from ninja import Router
from mmhci.core.services.person.list_people import ListPeopleService
from mmhci.core.apis.v1.schemas.person.person import PersonResponse

person_router = Router()

@person_router.get("", response=list[PersonResponse])
def list_people(request):
    people = ListPeopleService(request).execute()
    return people

@person_router.get("test")
def test_path(request):
    return {"test": "success"}

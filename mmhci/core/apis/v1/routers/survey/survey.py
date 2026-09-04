from ninja import Router

survey_router = Router()

@survey_router.get("")
def list_surveys(request):
    return {"surveys": ["Sample collection item"]}

@survey_router.get("/test")
def test_path(request):
    return {"test": "success"}

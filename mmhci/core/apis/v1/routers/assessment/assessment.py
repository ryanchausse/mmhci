from ninja import Router

assessment_router = Router()

@assessment_router.get("")
def list_assessments(request):
    return {"assessments": ["Sample collection item"]}

@assessment_router.get("/test")
def test_path(request):
    return {"test": "success"}

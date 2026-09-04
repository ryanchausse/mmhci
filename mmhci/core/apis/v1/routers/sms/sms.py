from ninja import Router

sms_router = Router()

@sms_router.get("")
def list_smss(request):
    return {"smss": ["Sample collection item"]}

@sms_router.get("/test")
def test_path(request):
    return {"test": "success"}

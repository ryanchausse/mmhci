from ninja import Router

log_router = Router()

@log_router.get("")
def list_logs(request):
    return {"logs": ["Sample collection item"]}

@log_router.get("/test")
def test_path(request):
    return {"test": "success"}

from ninja import Router

referral_router = Router()

@referral_router.get("")
def list_referrals(request):
    return {"referrals": ["Sample collection item"]}

@referral_router.get("/test")
def test_path(request):
    return {"test": "success"}

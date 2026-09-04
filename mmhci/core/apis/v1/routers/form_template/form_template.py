from ninja import Router

form_template_router = Router()

@form_template_router.get("")
def list_form_templates(request):
    return {"form_templates": ["Sample collection item"]}

@form_template_router.get("/test")
def test_path(request):
    return {"test": "success"}

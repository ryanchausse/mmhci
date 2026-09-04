from django.contrib.admin.views.decorators import staff_member_required
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja_extra.throttling import AnonRateThrottle, UserRateThrottle
from ninja_jwt.authentication import JWTAuth
from mmhci.core.apis.v1.routers.assessment.assessment import assessment_router
from mmhci.core.apis.v1.routers.consent.consent import consent_router
from mmhci.core.apis.v1.routers.contact.contact import contact_router
from mmhci.core.apis.v1.routers.form_template.form_template import form_template_router
from mmhci.core.apis.v1.routers.log.log import log_router
from mmhci.core.apis.v1.routers.note.note import note_router
from mmhci.core.apis.v1.routers.organisation.organisation import organisation_router
from mmhci.core.apis.v1.routers.person.person import person_router
from mmhci.core.apis.v1.routers.practitioner.practitioner import practitioner_router
from mmhci.core.apis.v1.routers.referral.referral import referral_router
from mmhci.core.apis.v1.routers.sms.sms import sms_router
from mmhci.core.apis.v1.routers.survey.survey import survey_router
from mmhci.core.apis.v1.routers.tag.tag import tag_router
from mmhci.core.apis.v1.routers.upload.upload import upload_router


api = NinjaExtraAPI(
    urls_namespace="api",
    auth=JWTAuth(),
    docs_decorator=staff_member_required,
    throttle=[
        AnonRateThrottle(),
        UserRateThrottle()
    ]
)

api.register_controllers(NinjaJWTDefaultController)
api.add_router("/users/", "mmhci.users.api.views.router")
api.add_router("/assessments/", assessment_router)
api.add_router("/consents/", consent_router)
api.add_router("/contacts/", contact_router)
api.add_router("/form_templates/", form_template_router)
api.add_router("/logs/", log_router)
api.add_router("/notes/", note_router)
api.add_router("/organisations/", organisation_router)
api.add_router("/people/", person_router)
api.add_router("/practitioners/", practitioner_router)
api.add_router("/referrals/", referral_router)
api.add_router("/smses/", sms_router)
api.add_router("/tags/", tag_router)
api.add_router("/uploads/", upload_router)

# Routes are protected by default, can override auth like so:
@api.get("/ping", auth=None)
def ping(request):
    return {"success": True}

from django.urls import path, include
app_name = "core"
urlpatterns = [
    path(
        "assessment/",
        include(
            ("mmhci.core.urls.assessment.assessment", "assessment"),
            namespace="assessment"
        ),
    ),
    path(
        "consent/",
        include(("mmhci.core.urls.consent.consent", "consent"), namespace="consent"),
    ),
    path(
        "contact/",
        include(("mmhci.core.urls.contact.contact", "contact"), namespace="contact"),
    ),
    path(
        "form_template/",
        include(
            ("mmhci.core.urls.form_template.form_template", "form_template"),
            namespace="form_template"
        ),
    ),
    path(
        "log/",
        include(("mmhci.core.urls.log.log", "log"), namespace="log"),
    ),
    path(
        "note/",
        include(("mmhci.core.urls.note.note", "note"), namespace="note"),
    ),
    path(
        "organisation/",
        include(
            ("mmhci.core.urls.organisation.organisation", "organisation"),
            namespace="organisation"
        ),
    ),
    path(
        "person/",
        include(("mmhci.core.urls.person.person", "person"), namespace="person"),
    ),
    path(
        "policy/",
        include(("mmhci.core.urls.policy.policy", "policy"), namespace="policy"),
    ),
    path(
        "practitioner/",
        include(
            ("mmhci.core.urls.practitioner.practitioner", "practitioner"),
            namespace="practitioner"
        ),
    ),
    path(
        "referral/",
        include(
            ("mmhci.core.urls.referral.referral", "referral"),
            namespace="referral"
        ),
    ),
    path(
        "role/",
        include(("mmhci.core.urls.role.role", "role"), namespace="role"),
    ),
    path(
        "sms/",
        include(("mmhci.core.urls.sms.sms", "sms"), namespace="sms"),
    ),
    path(
        "survey/",
        include(("mmhci.core.urls.survey.survey", "survey"), namespace="survey"),
    ),
    path(
        "tag/",
        include(("mmhci.core.urls.tag.tag", "tag"), namespace="tag"),
    ),
    path(
        "upload/",
        include(("mmhci.core.urls.upload.upload", "upload"), namespace="upload"),
    )
]
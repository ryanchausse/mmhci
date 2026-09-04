from django.urls import path, include
from django.views.generic import TemplateView

app_name = "core"
urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="adminlte_4_1/mmhci/dashboard/dashboard.html"),
        name="dashboard"
    ),
    path(
        "assessments/",
        include(
            ("mmhci.core.urls.assessment.assessment", "assessment"),
            namespace="assessments"
        ),
    ),
    path(
        "consents/",
        include(("mmhci.core.urls.consent.consent", "consent"), namespace="consents"),
    ),
    path(
        "contacts/",
        include(("mmhci.core.urls.contact.contact", "contact"), namespace="contacts"),
    ),
    path(
        "form_templates/",
        include(
            ("mmhci.core.urls.form_template.form_template", "form_template"),
            namespace="form_templates"
        ),
    ),
    path(
        "logs/",
        include(("mmhci.core.urls.log.log", "log"), namespace="logs"),
    ),
    path(
        "notes/",
        include(("mmhci.core.urls.note.note", "note"), namespace="notes"),
    ),
    path(
        "organisations/",
        include(
            ("mmhci.core.urls.organisation.organisation", "organisations"),
            namespace="organisation"
        ),
    ),
    path(
        "people/",
        include(("mmhci.core.urls.person.person", "person"), namespace="people"),
    ),
    path(
        "practitioners/",
        include(
            ("mmhci.core.urls.practitioner.practitioner", "practitioner"),
            namespace="practitioners"
        ),
    ),
    path(
        "referrals/",
        include(
            ("mmhci.core.urls.referral.referral", "referral"),
            namespace="referrals"
        ),
    ),
    path(
        "smses/",
        include(("mmhci.core.urls.sms.sms", "sms"), namespace="smses"),
    ),
    path(
        "surveys/",
        include(("mmhci.core.urls.survey.survey", "survey"), namespace="surveys"),
    ),
    path(
        "tags/",
        include(("mmhci.core.urls.tag.tag", "tag"), namespace="tags"),
    ),
    path(
        "uploads/",
        include(("mmhci.core.urls.upload.upload", "upload"), namespace="uploads"),
    )
]
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from .api import api

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="main_template_files/index.html"),
        name="home",
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("mmhci.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("core/", include("mmhci.core.urls.core", namespace="core")),
    # Your stuff: custom urls includes go here
    path(
        "assessment/",
        include("mmhci.core.urls.assessment", namespace="assessment"),
    ),
    path(
        "consent/",
        include("mmhci.core.urls.consent", namespace="consent"),
    ),
    path(
        "contact/",
        include("mmhci.core.urls.contact", namespace="contact"),
    ),
    path(
        "form_template/",
        include(
            "mmhci.core.urls.form_template", namespace="form_template"
        ),
    ),
    path(
        "log/",
        include("mmhci.core.urls.log", namespace="log"),
    ),
    path(
        "note/",
        include("mmhci.core.urls.note", namespace="note"),
    ),
    path(
        "organisation/",
        include("mmhci.core.urls.organisation", namespace="organisation"),
    ),
    path(
        "person/",
        include("mmhci.core.urls.person", namespace="person"),
    ),
    path(
        "policy/",
        include("mmhci.core.urls.policy", namespace="policy"),
    ),
    path(
        "practitioner/",
        include("mmhci.core.urls.practitioner", namespace="practitioner"),
    ),
    path(
        "referral/",
        include("mmhci.core.urls.referral", namespace="referral"),
    ),
    path(
        "role/",
        include("mmhci.core.urls.role", namespace="role"),
    ),
    path(
        "sms/",
        include("mmhci.core.urls.sms", namespace="sms"),
    ),
    path(
        "survey/",
        include("mmhci.core.urls.survey", namespace="survey"),
    ),
    path(
        "tag/",
        include("mmhci.core.urls.tag", namespace="tag"),
    ),
    path(
        "third_party_service/",
        include(
            "mmhci.core.urls.third_party_service",
            namespace="third_party_service",
        ),
    ),
    path(
        "upload/",
        include("mmhci.core.urls.upload", namespace="upload"),
    ),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


# API URLS
urlpatterns += [
    # API base url
    path("api/", api.urls),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            *urlpatterns,
        ]

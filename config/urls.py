from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from .api import api

urlpatterns = [
    # Likely moving this path into the main core app. Leaving alone for now.
    path(
        "",
        TemplateView.as_view(template_name="adminlte_4_1/mmhci/dashboard/dashboard.html"),
        name="home",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("mmhci.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Core app URLs live at the root
    path("", include("mmhci.core.urls", namespace="core")),
    # Your stuff: custom urls includes go here
    # (These have been moved from /mmhci/core/urls.py into the core app -
    # see __init__.py in /mmhci/core/urls directory)
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

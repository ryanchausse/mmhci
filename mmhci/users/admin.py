from allauth.account.decorators import secure_admin_login
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "preferred_org",
                    "owning_organisation",
                    "created_by",
                    "updated_by",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("uuid", "created_at", "updated_at")
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    # Intercepts creating a new User via the Admin interface, sets an unusable
    # password, creates a secure token, and emails it to the new User
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        if is_new:
            obj.set_unusable_password()

        # Save user to DB first so they get an ID
        super().save_model(request, obj, form, change)

        if is_new:
            token_generator = EmailAwarePasswordResetTokenGenerator()
            token = token_generator.make_token(obj)
            uid36 = user_pk_to_url_str(obj)
            setup_path = reverse(
                "account_reset_password_from_key",
                kwargs={"uidb36": uid36, "key": token},
            )

            # port 8005 is in docker-compose.local.yml; need to abstract into a setting
            if settings.DEBUG:
                current_domain = "127.0.0.1:8005"
                protocol = "http"
            else:
                current_domain = Site.objects.get_current().domain
                protocol = "https"

            invite_url = f"{protocol}://{current_domain}{setup_path}"

            send_mail(
                subject="MMHCI Account Invitation",
                message=f"Welcome to MMHCI. Create your password here: {invite_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email],
                fail_silently=False,
            )

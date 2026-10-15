import uuid
from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.db.models import ForeignKey
from django.db.models import UUIDField
from django.db.models import PROTECT
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for MMHCI.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    uuid = UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]
    preferred_org = ForeignKey(
        "core.Organisation", on_delete=PROTECT, null=True, blank=True
    )
    owning_organisation = ForeignKey(
        "core.Organisation",
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_owning_org"
    )
    created_by = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by",
    )
    updated_by = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated_by",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def has_org_permission(self, organisation_id, permission_codename):
        """
        Checks if the user belongs to any group inside the organisation
        that grants them the required permission via their assigned role.
        """
        # Query the OrganisationMembership table
        return self.user_memberships.filter(
            organisation_group__organisation_id=organisation_id,
            organisation_role__permissions__codename=permission_codename
        ).exists()

    class Meta:
        permissions = [
            (
                'can_view_user_list',
                'Can view a list of users'
            ),
        ]

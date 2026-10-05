from typing import Dict, Set
from django.core.exceptions import ImproperlyConfigured


# Note that Celery and tests would only need to pass an org_perms dict
# In web session and API usage, request.org_perms is where this is located
class OrgPermissionsRequiredBaseService:
    required_permissions: frozenset[str] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.required_permissions is None:
            raise ImproperlyConfigured(
                f"Service class '{cls.__name__}' must define a "
                f"'required_permissions' frozenset."
            )

    def __init__(self, org_perms: Dict[int, Set[str]]):
        self.org_perms = org_perms
        self.authorized_org_ids = self._permitted_organisation_ids()

    def _permitted_organisation_ids(self) -> Set[int]:
        return {
            org_id
            for org_id, granted_permissions in self.org_perms.items()
            if self.required_permissions <= granted_permissions
        }

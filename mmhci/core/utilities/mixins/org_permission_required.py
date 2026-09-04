from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class OrgPermissionRequiredMixin(AccessMixin):
    """
    Checks if the user has the required permission code via their
    assigned role within the organization context.
    """
    # Set this in the View (e.g., 'change_organisation')
    required_permissions = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        org_id = kwargs.get('org_id')
        if not org_id:
            raise PermissionDenied("Organisation context is missing")

        # Check permissions dynamically through the User helper method
        if not request.user.has_org_permission(org_id, self.required_permissions):
            raise PermissionDenied(
                "You do not have the required permissions in this organisation."
            )

        return super().dispatch(request, *args, **kwargs)

# Create an org_perms dict that has all permissions in all orgs for the user.
# This is basically a cache of permissions for a user refreshed on every HTTP request.
# Accessible in views/api views with self.request.org_perms
# Still need to handle the superuser case


class OrgPermissionsCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.org_perms = {}
            return self.get_response(request)

        memberships = (
            request.user.org_group_memberships
            .select_related("organisation_group__organisation")
            .prefetch_related("organisation_group__roles__permissions__content_type")
        )

        org_perms = {}

        for membership in memberships:
            group = membership.organisation_group
            org_id = group.organisation_id

            org_perms.setdefault(org_id, set())

            for role in group.roles.all():
                for perm in role.permissions.all():
                    org_perms[org_id].add(
                        f"{perm.content_type.app_label}.{perm.codename}"
                    )

        request.org_perms = org_perms
        return self.get_response(request)

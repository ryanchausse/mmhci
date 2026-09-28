# Create an org_perms dict that has all permissions in all orgs for the user.
# This is basically a cache of permissions for a user per HTTP request.

class OrgPermissionsCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.org_perms = {}
        else:
            # Gets all permissions in all orgs
            memberships = request.user.group_memberships.select_related('organisation').prefetch_related(
                'roles__permissions__content_type'
            )

            org_perms = {}
            for membership in memberships:
                org_id = membership.organisation_id
                if org_id not in org_perms:
                    org_perms[org_id] = set()

                for role in membership.roles.all():
                    for perm in role.permissions.all():
                        org_perms[org_id].add(f"{perm.content_type.app_label}.{perm.codename}")

            request.org_perms = org_perms

        return self.get_response(request)

# Create a current org context variable that uses DB session persistence.
# Assignable in web views with request.session["current_org_id"] = 0
# Still need to handle the API session case and the superuser case


class CurrentOrgMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.session["current_org_id"] = None
            return self.get_response(request)

        # Might want to handle receipt of X-Current-Org-Id if request
        # is coming from API and there is no default user org
        if not request.session.get("current_org_id"):
            user_preferred_org = request.user.preferred_org
            if user_preferred_org and request.org_perms.get(user_preferred_org.id):
                request.session["current_org_id"] = user_preferred_org.id
            elif len(request.org_perms) == 1:
                request.session["current_org_id"] = next(iter(request.org_perms), None)
            else:
                request.session["current_org_id"] = None

        return self.get_response(request)

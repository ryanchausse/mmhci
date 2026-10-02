# Create a current org context variable that uses DB session persistence.
# Assignable in web views with request.session["current_org_id"] = x
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
            # TODO: get default org for user for initialisation here
            request.session["current_org_id"] = 1

        return self.get_response(request)

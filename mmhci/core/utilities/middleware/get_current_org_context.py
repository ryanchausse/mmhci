# Sets or persists the current org context for a user session. Provides
# a header param "X-Current-Org-ID" for API requests if needed. Runs with
# a context var because it needs to be persisted to the DB-backed session

from contextvars import copy_context, ContextVar

current_org_id: ContextVar[str | None] = ContextVar(
    "current_org_id", default=None
)


class CurrentOrgMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_org = request.session.get("current_org_id")
        if not current_org:
            current_org = request.headers.get("X-Current-Org-ID")
            if current_org:
                request.session["current_org_id"] = current_org

        # This is thread safe and gets destroyed on crash
        # (similar to a "with:" context manager)
        ctx = copy_context()
        def execute_isolated():
            current_org_id.set(current_org)
            return self.get_response(request)

        return ctx.run(execute_isolated)

from django.contrib.auth.middleware import LoginRequiredMiddleware


class CoreLoginRequiredMiddleware(LoginRequiredMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        resolver_match = request.resolver_match

        if resolver_match is None or "core" not in resolver_match.namespaces:
            return None

        return super().process_view(request, view_func, view_args, view_kwargs)

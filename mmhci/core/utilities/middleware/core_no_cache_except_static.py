# core/middleware.py
from django.conf import settings
from django.utils.cache import patch_cache_control


# This is a privacy measure - add "no cache" headers unless serving static files
class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith(settings.STATIC_URL):
            return response

        patch_cache_control(
            response, 
            no_cache=True, 
            no_store=True, 
            must_revalidate=True, 
            private=True
        )
        return response

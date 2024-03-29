from django.http import HttpResponse
from core import settings


class KillFaviconMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/favicon.ico':
            return HttpResponse(status=204)
        return self.get_response(request)


class SiteDocumentFileAccessMiddleware:
    """

    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path
        if path.startswith(settings.DOCUMENT_URL):
            if not user.is_staff:
                return HttpResponse(status=403)
        response = self.get_response(request)
        return response

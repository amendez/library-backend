import os

from django.http import JsonResponse


class CheckTokenMiddleware:
    """
    Middleware for checking the token in the request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.headers.get("Authorization", None)

        if not access_token:
            return JsonResponse(
                {"error": "No access token provided"},
                status=401
            )

        token = os.environ.get('ACCESS_TOKEN', 'ZYyijAo2MEk4VSaTGC6VJiU7CRWBJeuDPg7oPksSkztV8')
        if access_token != f"Bearer {token}":
            return JsonResponse(
                {"error": "Invalid access token"},
                status=401
            )

        return self.get_response(request)

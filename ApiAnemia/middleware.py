from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import base64

protected_endpoints = [
    "/auth/register/google"
]

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        if request.path not in protected_endpoints:
            # Skip the middleware for the /auth endpoint
            return self.get_response(request)
        
        token = request.headers.get('Authorization', None)

        if not token:
            return HttpResponse('No Autorizado', status=401)
        
        if token.startswith('Bearer '):
            token = token.replace('Bearer ', '')

        tokenBytes = base64.b64decode(token)

        token = tokenBytes.decode('utf-8')

        user = Token.objects.get(key=token).user

        if user:
            request.userdb = user
            return self.get_response(request)   
        
        return HttpResponse('No Autorizado', status=401)
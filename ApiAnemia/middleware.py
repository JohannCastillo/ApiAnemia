from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import base64

protected_endpoints = [
    "/auth/register/google",
    "/pacientes/apoderado/user/create",
    "/pacientes/apoderado/user",
    "/diagnosticos/user",
]


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)

        # Verificar si la ruta es parte del módulo chatbots o está en la lista de rutas protegidas
        if (
            request.path.startswith("/chatbot/")
            or request.path.startswith("/image-generator/")
            or request.path in protected_endpoints
        ):
            token = request.headers.get("Authorization", None)

            if not token:
                return HttpResponse("No Autorizado", status=401)

            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")

            try:
                tokenBytes = base64.b64decode(token)
                token = tokenBytes.decode("utf-8")
                user = Token.objects.get(key=token).user
                if user:
                    request.userdb = user
                    return self.get_response(request)
            except (Token.DoesNotExist, Exception):
                pass  # Handle any exceptions, like decoding issues or invalid tokens

            return HttpResponse("No Autorizado", status=401)

        return self.get_response(request)

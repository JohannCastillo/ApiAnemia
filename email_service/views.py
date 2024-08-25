from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email_service.utils.email import attach_image

from django.conf import settings
import os
BASE_DIR = settings.BASE_DIR
static_path = os.path.join(BASE_DIR, 'email_service', 'static')

# Create your views here.
@api_view(['POST'])
def send_email(request):
    try:
        to_email = request.data.get('to_email', 'johannjco15022@gmail.com')
        subject = request.data.get('subject', 'Api Anemia')
        message = request.data.get('message', 'Hola, este es un mensaje de prueba')
        template = request.data.get('template')
        email = EmailMultiAlternatives(subject, message, None, [to_email])
        if template is not None:
            email.attach_alternative(template, 'text/html')

        email.send()

        return Response({
            "message": "Email enviado correctamente"
        },status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error al enviar el email: {e}")
        return Response({
            "message": "Error al enviar el email"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# """
#     Función de uso interno: 
#     Enviar un mensaje de diagnostico a un usuario por email o whatsapp
#     params : 
#     @diagnostic : Objeto diagnostico
#     @message_options : Opciones de mensaje : dict
#         - service : tipo de servicio ["email", "whatsapp"]
#         - subject : asunto del mensaje
# """

# def send_diagnostic_message(diagnostic, message_options):
#     try:

        
#     except Exception as e:
#         print(f"Error al enviar el email: {e}")
#         return Response({
#             "message": "Error al enviar el email"
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
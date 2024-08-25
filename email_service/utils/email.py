from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
import os
BASE_DIR = settings.BASE_DIR
static_path = os.path.join(BASE_DIR, 'email_service', 'static')

def send_diagnostic_email(diagnostic, options):
     try:
        email = EmailMultiAlternatives(options['subject'], options['message'], None, [options['to_email']])
        template = render_to_string('diagnostic_template.html', {
            'diagnostic': diagnostic,
        })
        email.attach_alternative(template, 'text/html')
        images = [
            'logo.png',
            'kid.png',
            'ruler-measure-2.png',
            'heart-rate-monitor.png',
            'milk.png',
            'droplet-exclamation.png',
            'weight.png',
        ]
        for image in images:
            image_path = os.path.join(static_path, 'img', image)
            attach_image(email, image_path, image)
        email.send()
        print("Email enviado correctamente")
     except Exception as e:
         print(f"Error al enviar el email: {e}")
     

"""
Inserta una imagen en una plantilla html de un email
@params email: objeto de tipo EmailMultiAlternatives
@params image_path: ruta del archivo de la imagen
"""
def attach_image(email : EmailMultiAlternatives, image_path : str, image_cid : str):
    with open(image_path, 'rb') as img_file:
        image = MIMEImage(img_file.read())
        image.add_header('Content-ID', f'<{image_cid}>')
        email.attach(image)


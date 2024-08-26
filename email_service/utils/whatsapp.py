import datetime
import threading
import requests

from ApiAnemia.settings import WHATSAPP_API_TOKEN, WHATSAPP_API_URL
from api.models import Apoderado, Diagnostico, Paciente

def async_send_diagnostic_whatsapp(diagnostic: Diagnostico, paciente: Paciente, apoderado: Apoderado):
    thread = threading.Thread(target=send_diagnostic_whatsapp, args=(diagnostic, paciente, apoderado))
    thread.start()

def send_diagnostic_whatsapp(diagnostic: Diagnostico, paciente: Paciente, apoderado: Apoderado):
    url = WHATSAPP_API_URL
    token = WHATSAPP_API_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    recomendacion = "Ir a centro de salud"
    if diagnostic.dx_anemia.nivel == "Normal":
        recomendacion = "Seguir así. Felicidades"
    elif diagnostic.dx_anemia.nivel == "Anemia Leve":
        recomendacion = "Mejorar alimentación y asistir al centro de salud"
    elif diagnostic.dx_anemia.nivel == "Anemia Moderada":
        recomendacion = "Asistir urgente al centro de salud"
    elif diagnostic.dx_anemia.nivel == "Anemia Severa":
        recomendacion = "Asistir urgente al centro de salud. Actuar a tiempo será vital"


    data = build_diangostic_template(apoderado.nombre, apoderado.telefono, paciente.nombre, diagnostic.edad_meses, diagnostic.created_at, diagnostic.dx_anemia.nivel, diagnostic.peso, diagnostic.talla, diagnostic.suplementacion, recomendacion)
    print(data)
    response = requests.post(url, headers=headers, json=data)
    print("Whatsapp enviado")

def build_diangostic_template(apoderado: str, telefono, paciente:str, edad, fecha:datetime, diangostico:str, peso:float, talla:float, suplementacion:bool, recomendacion:str):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"51{telefono}",
        "type": "template",
        "template": {
            "name": "notificacion_anemia",
            "language": {
                "code": "es_MX"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": apoderado},
                        {"type": "text", "text": paciente},
                        {"type": "text", "text": str(edad)},
                        {"type": "text", "text": fecha.strftime("%d/%m/%Y")},
                        {"type": "text", "text": diangostico},
                        {"type": "text", "text": str(peso)},
                        {"type": "text", "text": str(talla)},
                        {"type": "text", "text": "Sí" if suplementacion else "No"},
                        {"type": "text", "text": recomendacion},
                    ]
                }
            ]
        }   
    }
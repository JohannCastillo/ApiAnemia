from email_service.utils.email import async_send_diagnostic_email
from api.models import Apoderado, Paciente, Diagnostico
from email_service.utils.whatsapp import async_send_diagnostic_whatsapp

"""
Enviar alertas por email o whatsapp según preferencias del usuario
"""

def alert_diagnostic_to_apoderados(paciente : Paciente, diagnostico: Diagnostico):
    try:
        apoderados = Apoderado.objects.filter(apoderado_paciente__paciente=paciente)
        # TODO : Decidir si enviar por email o whatsapp según las preferncias del usuario accediendo por el user_id (por ahora no)
        for apoderado in apoderados:
            print(f"Enviando email a : {apoderado.email}")

            if diagnostico.dx_anemia.nivel != "Normal":
                async_send_diagnostic_email(diagnostico, options={
                'to_email': apoderado.email,
                'subject': f'Diagnóstico de nivel de anemia del paciente {paciente.nombre}',
                'message': 'Resultado de la predicción del modelo de anemia del paciente'
                })

            async_send_diagnostic_whatsapp(diagnostico, paciente, apoderado)

    except Exception as e:
        print(f"Error al enviar alerta {e}")



# def alert_whatsapp_diagnostic_to_apoderados(paciente : Paciente, diagnostico: Diagnostico):
#     try:
#         apoderados = Apoderado.objects.filter(apoderado_paciente__paciente=paciente)
#         # TODO : Decidir si enviar por email o whatsapp según las preferncias del usuario accediendo por el user_id (por ahora no)
#         for apoderado in apoderados:
#             print(f"Enviando whatsapp a : {apoderado.email}")

            
#     except Exception as e:
#         print(f"Error al enviar el email {e}")
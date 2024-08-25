from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from api.models import Dieta
from api.pagination.pageable import CustomPagination, paginate_results
from chatbot.utils.dieta_gpt import DICTIONARY_DIETA, DIETA_PROMPT, RESULTADOS_DIETA
from models.utils.diagnostico_utils import calcular_edad_en_meses
from .models import Conversation, ConversationDieta, ConversationType, Message, RoleMessage
from .serializers import ConversationDetailSerializer, ConversationListSerializer, ConversationSerializer, MessageSerializer
from openai import OpenAI
from django.conf import (
    settings,
)  # Para obtener las configuraciones de tu archivo settings.py


client = OpenAI(api_key=settings.OPENAI_API_KEY)
from django.conf import (
    settings,
)  # Para obtener las configuraciones de tu archivo settings.py

@api_view(["GET"])
def get_messages(request, id):
    user = request.userdb
    
    messages = Message.objects.filter(
        conversation_id=id, 
        conversation__user=user,
        role__in=[RoleMessage.USER, RoleMessage.BOT]
    ).order_by("created_at")

    return Response(
        paginate_results(CustomPagination(), request, messages, MessageSerializer)
    , status=200)


@api_view(["GET"])
def get_conversation_details(request, id):
    user = request.userdb
    conversation = Conversation.objects.filter(user=user, id=id).first()

    if not conversation:
        return Response({"error": "Conversation not found"}, status=404)
    
    if conversation.type == ConversationType.DIETA:
        conversation_dieta = ConversationDieta.objects.get(conversation=conversation)
        conversation.dieta = conversation_dieta

    return Response({
        "conversation": ConversationDetailSerializer(conversation).data
    })

@api_view(["GET"])
def get_conversations(request):
    user = request.userdb
    conversations = Conversation.objects.filter(user=user)
    return Response(
        paginate_results(CustomPagination(), request, conversations, ConversationListSerializer)
    , status=200)


@api_view(["POST"])
def create_conversation(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = ConversationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

    
@api_view(["POST"])
def create_conversation_dieta(request, dieta_id):
    user = request.userdb

    dieta = Dieta.objects.select_related("paciente").get(id=dieta_id)

    paciente = dieta.paciente

    string_dieta = ""
    meses = calcular_edad_en_meses(paciente.fecha_nacimiento)

    for key, value in dieta.__dict__.items():
        if key.startswith("frec"):
            string_dieta += f"{DICTIONARY_DIETA[key]}: {value}\n"

    # Crear una conversación con la dieta del paciente
    conversation = Conversation.objects.create(user=user, type=ConversationType.DIETA)

    ConversationDieta.objects.create(conversation=conversation, dieta=dieta)

    messages = [
#         {
#             "role": "system", 
#             "content": """Brinda recomendaciones para mejorar el nivel de anemia del paciente según su dieta. 
# El usuario te dara la frecuencia de consumo de ciertos alimentos, estos estarán en un rango
# de 0 y 7 que significa la cantidad de dias de la semana ha consumido ese alimento. 
# Previmante, se ha hecho una predicción de la probabilidad que este usuario vaya a tener anemia.
# Si tiene una buena alimentación, felicítalo e igual brindale algunas recomendaciones 
# de como puede mejorar.
# Asegurate de dar recomendaciones cortas.
# Recomienda algunos platos de Perú que puedan ayudar a mejorar su dieta.
# El estudio que se hace es hacia niños de 6 a 36 meses.
# El usuario que ingresa los datos puede ser un padre de familia o apoderado. Pero siempre refierete al hijo como "paciente".
# Los datos que te dan son de su hijo o cualquier otro paciente."""
#         },
        {
            "role": "system",
            "content": f"Nombre: {paciente.nombre} - Edad en meses: {meses} - Sexo: {paciente.sexo}"
        },
        {
            "role": "user", 
            "content": string_dieta
        }, 
        {
            "role": "system",
            "content": "Predicción hecha por el sistema " + RESULTADOS_DIETA[dieta.dx_dieta]
        }
    ]

    for message in messages:
        Message.objects.create(
            conversation=conversation, content=message["content"], role=message["role"]
        )

    return Response({
        "conversation_id": conversation.id
    })


@api_view(["GET"])
def get_conversation(request, user_id, pk):
    user = get_object_or_404(User, id=user_id)
    conversation = get_object_or_404(Conversation, pk=pk, user=user)
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data)

@api_view(["GET"])
def get_messages(request, conv_id):
    user = request.userdb
    conversation = get_object_or_404(Conversation, pk=conv_id, user=user)
    messages = Message.objects.filter(conversation=conversation, role__in=[RoleMessage.USER, RoleMessage.BOT])
    return Response(MessageSerializer(messages, many=True).data)

@api_view(["POST"])
def chat(request, conv_id):
    user = request.userdb
    conversation = get_object_or_404(Conversation, pk=conv_id, user=user)

    messages = Message.objects.filter(conversation=conversation)

    if messages.count() <= 3:
        pass
    else :
        user_message = request.data.get("message")

        Message.objects.create(
            conversation=conversation, content=user_message, role=RoleMessage.USER
        )

    bot_response = get_bot_response(conversation)

    bot_message = Message.objects.create(
        conversation=conversation, content=bot_response, role=RoleMessage.BOT
    )

    return Response(MessageSerializer(bot_message).data)


# Configura tu clave API en settings.py


def get_bot_response(conversation: Conversation):
    """
    Genera una respuesta de bot manteniendo el contexto de la conversación.
    """
    try:
        # Recuperar todos los mensajes de la conversación ordenados por timestamp
        messages = Message.objects.filter(conversation=conversation).order_by(
            "created_at"
        )

        # Crear una lista de historial de mensajes para la API de OpenAI
        chat_history = []

        # Agregar un mensaje del sistema opcional para establecer el comportamiento del asistente
        if conversation.type == ConversationType.DIETA:
            chat_history.append({"role": "system", "content": DIETA_PROMPT})

        # Iterar sobre los mensajes de la conversación y agregar al historial
        for message in messages:
            print(message.content)
            role = "assistant" if message.role == RoleMessage.BOT else message.role
            chat_history.append({"role": role, "content": message.content})

        # Llamada a la API de OpenAI para obtener una respuesta con el historial completo
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Puedes elegir el modelo adecuado según tu plan de API
            messages=chat_history,
            temperature=0.7,
        )

        # Extrae la respuesta del bot
        bot_response = response.choices[0].message.content.strip()
        return bot_response

    except Exception as e:
        # Manejo básico de errores
        print(e)
        return "Lo siento, ha ocurrido un error al intentar procesar tu solicitud."

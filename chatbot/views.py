from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from openai import OpenAI
from django.conf import (
    settings,
)  # Para obtener las configuraciones de tu archivo settings.py


client = OpenAI(api_key=settings.OPENAI_API_KEY)
from django.conf import (
    settings,
)  # Para obtener las configuraciones de tu archivo settings.py


@api_view(["GET"])
def get_conversations(request, user_id):
    user = get_object_or_404(User, id=user_id)
    conversations = Conversation.objects.filter(user=user)
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_conversation(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = ConversationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def get_conversation(request, user_id, pk):
    user = get_object_or_404(User, id=user_id)
    conversation = get_object_or_404(Conversation, pk=pk, user=user)
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data)


@api_view(["POST"])
def chat(request, user_id, pk):
    user = get_object_or_404(User, id=user_id)
    conversation = get_object_or_404(Conversation, pk=pk, user=user)

    user_message = request.data.get("message")

    # Crear el mensaje del usuario
    Message.objects.create(
        conversation=conversation, content=user_message, is_user=True
    )

    # Generar respuesta del bot con el contexto completo de la conversación
    bot_response = get_bot_response(conversation)

    # Crear el mensaje del bot
    bot_message = Message.objects.create(
        conversation=conversation, content=bot_response, is_user=False
    )

    return Response(MessageSerializer(bot_message).data)


# Configura tu clave API en settings.py


def get_bot_response(conversation):
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
        chat_history.append({"role": "system", "content": "Eres un asistente útil."})

        # Iterar sobre los mensajes de la conversación y agregar al historial
        for message in messages:
            role = "user" if message.is_user else "assistant"
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

from rest_framework import serializers

from api.serializers.Dieta import DietaSerializer
from .models import Conversation, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "content", "role", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "user", "messages", "created_at", "updated_at"]

class ConversationListSerializer(serializers.ModelSerializer):
    last_message_content = serializers.SerializerMethodField()
    last_message_time = serializers.DateTimeField(read_only=True)
    last_message_role = serializers.CharField(read_only=True)

    def get_last_message_content(self, obj):
        return obj.last_message_content[:100] if obj.last_message_content else ''

    class Meta:
        model = Conversation
        fields = ['id', 'last_message_content', 'last_message_role', 'last_message_time', "created_at", "updated_at", "type"]


class ConversationDetailSerializer(serializers.ModelSerializer):
    dieta = serializers.SerializerMethodField()

    def get_dieta(self, obj):
        if obj.type == "dieta":
            return DietaSerializer(obj.dieta.dieta).data
        return None

    class Meta:
        model = Conversation
        fields = "__all__"

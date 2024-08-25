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

    class Meta:
        model = Conversation
        fields = ["id", "created_at", "updated_at", "type"]


class ConversationDetailSerializer(serializers.ModelSerializer):
    dieta = serializers.SerializerMethodField()

    def get_dieta(self, obj):
        if obj.type == "dieta":
            return DietaSerializer(obj.dieta.dieta).data
        return None

    class Meta:
        model = Conversation
        fields = "__all__"

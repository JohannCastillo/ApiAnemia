from django.db import models
from django.contrib.auth.models import User

from api.models import Dieta

class ConversationType(models.TextChoices):
    DIETA = 'dieta', 'Dieta'
    CHAT = 'chat', 'Chat'

class Conversation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=10,
        choices=ConversationType.choices,
        default=ConversationType.CHAT,
    )

class ConversationDieta(models.Model):
    conversation = models.OneToOneField(
        Conversation, on_delete=models.CASCADE, related_name="dieta"
    )
    dieta = models.ForeignKey(
        Dieta, on_delete=models.CASCADE, related_name="conversation"
    )


from django.db import models


class RoleMessage(models.TextChoices):
    SYSTEM = 'system', 'System'
    BOT = 'bot', 'Bot'
    USER = 'user', 'User'

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    role = models.CharField(
        max_length=10,
        choices=RoleMessage.choices,
        default=RoleMessage.USER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

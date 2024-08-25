from django.urls import path
from . import views

urlpatterns = [
    path(
        "conversations",
        views.get_conversations,
        name="get_conversation",
    ),
    path(
        "conversations/create/dieta/<int:dieta_id>",
        views.create_conversation_dieta,
        name="create_conversation",
    ),
    path(
        "conversations/<int:id>/",
        views.get_conversation_details,
        name="get_conversation",
    ),
    path(
        "conversations/<int:conv_id>/messages/",
        views.get_messages,
        name="get_conversation",
    ),
    path(
        "conversations/<int:user_id>/create/",
        views.create_conversation,
        name="create_conversation",
    ),
    path(
        "conversations/<int:user_id>/<int:pk>/",
        views.get_conversation,
        name="get_conversation",
    ),
    path("conversations/<int:conv_id>/chat/", views.chat, name="chat"),
]

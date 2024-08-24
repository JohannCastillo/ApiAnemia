from django.urls import path
from . import views

urlpatterns = [
    path(
        "conversations/<int:user_id>/",
        views.get_conversations,
        name="get_conversations",
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
    path("conversations/<int:user_id>/<int:pk>/chat/", views.chat, name="chat"),
]

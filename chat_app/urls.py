from django.urls import path, include
from rest_framework import routers

from chat_app.views import AuthView, ChatsView, MessagesView, receive_token

router = routers.SimpleRouter()
router.register('chats', ChatsView, basename="chats")
router.register('messages', MessagesView, basename="messages")

urlpatterns = [
  path('fcm/', receive_token),
  path('api/', include(router.urls)),
  path('api/auth', AuthView.as_view()),
] + router.urls

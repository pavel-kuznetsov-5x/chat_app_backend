from django.urls import path, include
from rest_framework import routers

from chat_app.views import AuthView, ChatsView, MessagesView, send_message

router = routers.SimpleRouter()
router.register('chats', ChatsView, basename="chats")
router.register('messages', MessagesView, basename="messages")

urlpatterns = [
  path('message/', send_message),
  path('api/', include(router.urls)),
  path('api/auth', AuthView.as_view()),
] + router.urls

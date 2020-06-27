from django.urls import path, include
from rest_framework import routers

from chat_app.views import AuthView, ChatsView

router = routers.SimpleRouter()
router.register('chats', ChatsView, basename="chats")

urlpatterns = [
  path('api/', include(router.urls)),
  path('api/auth', AuthView.as_view()),
] + router.urls

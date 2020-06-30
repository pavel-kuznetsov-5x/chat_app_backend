from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import FormView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from chat_app import models


# todo optimize requests
from chat_app.models import Chat, Message


class ChatSerializer(ModelSerializer):
    display_name = SerializerMethodField()
    avatar_url = CharField(default="https://miro.medium.com/max/256/1*d69DKqFDwBZn_23mizMWcQ.png")

    class Meta:
        model = Chat
        fields = ['id', 'display_name', 'avatar_url']

    def get_display_name(self, obj):
        if obj.group:
            return obj.name
        else:
            current_user = self.context["request"].user
            other_user = obj.users.exclude(id=current_user.id).first()
            return other_user.username


class ChatsView(ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.chat_set.all()


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'text', 'from_user']


class MessagesView(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(chat_id=self.request.GET["chat_id"])


class AuthView(APIView):

    def post(self, request, **kwargs):
        if "username" in request.data and "password" in request.data:
            user = authenticate(username=request.data["username"], password=request.data["password"])
            if user:
                login(request, user)
                token = Token.objects.filter(user=user).first()
                if not token:
                    token = Token.objects.create(user=user)
                return Response(data={
                    "token": token.key,
                    "user_id": user.id
                }, status=status.HTTP_200_OK)
        # else:
        #     if "token" in request.data:
        #         google_id_token = request.data["token"]
        #         # todo validate id token
        #         # todo get email
        #         email = "mail@com.ua"
        #         auth_data = AuthData.objects.filter(google_user_id=google_id_token).first()
        #         if not auth_data:
        #             user = User.objects.filter(email=email).first()
        #             if not user:
        #                 user = User(username=email, email=email, password="123").save()
        #             token = Token.objects.create(user=user)
        #             AuthData(google_user_id=google_id_token, user=user).save()
        #         else:
        #             user = User.objects.filter(id=auth_data.user.id).first()
        #             token = Token.objects.filter(user=user).first()
        #         login(request, user)
        #         return Response(data={"token": token.key}, status=status.HTTP_501_NOT_IMPLEMENTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

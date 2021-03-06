from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, TextField, BooleanField, ForeignKey, CASCADE, ManyToManyField


class Chat(Model):
    name = TextField(default="")
    group = BooleanField(default=False)
    users = ManyToManyField(User)


class Message(Model):
    text = TextField()
    chat = ForeignKey(Chat, on_delete=CASCADE)
    author = ForeignKey(User, on_delete=CASCADE)

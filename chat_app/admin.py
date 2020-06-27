from django.contrib import admin

# Register your models here.
from chat_app import models

admin.site.register(models.Chat)
admin.site.register(models.Message)

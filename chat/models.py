from __future__ import unicode_literals
from swampdragon.models import SelfPublishModel
from django.db import models
from core.models import Admin
from .serializers import ChatSerializer


class Chat(SelfPublishModel, models.Model):
        serializer_class = ChatSerializer
        user = models.ForeignKey(Admin)
        message = models.TextField()

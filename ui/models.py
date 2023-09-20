import uuid
from django.utils import timezone
from django.db import models

# Create your models here.

class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    json = models.JSONField()

class Conversation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    title = models.TextField(max_length=255, null=False, blank=False)
    


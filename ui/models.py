import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
GENERATION_STATES = [
    ("finished", _("finished")),
    ("unfinished", _("unfinished")),
    ("failed", _("failed")),
]

class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    json = models.JSONField()
    model = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(choices=GENERATION_STATES, blank=False, null=False)

class Conversation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255, null=False, blank=False)
    
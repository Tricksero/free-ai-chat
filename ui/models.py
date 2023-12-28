import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

# some predefined states questions can have
GENERATION_STATES = [
    ("new", _("new")), # should indicate that this object was newly created and has an empty response
    ("finished", _("finished")), # answer generation complete, polling can be stopped
    ("unfinished", _("unfinished")), # answer generation incomplete, either polling still in progress or interrupted
    ("failed", _("failed")), # indicates that the generation server had an error
]

class Question(models.Model):
    """
    Model that saves all data about a question-answer interaction in a format that
    can easily be used to display a chat log in the frontend.
    TODO: Look how the models expect logs to be passed onto them and provide serializers.
    """
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    json = models.JSONField()
    answer = models.CharField(default="", null=False, blank=False)
    question = models.CharField(null=False, blank=False)
    model = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(default="new", choices=GENERATION_STATES, blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question

class Conversation(models.Model):
    """
    Model that saves basic information about a conversation to be displayed in a list to the left.
    TODO: Connect this to a user.
    """
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255, null=False, blank=False)
    
class LanguageModel(models.Model):
    """
    Names of models available to chat with.
    TODO: Maybe use fixtures, APIs or create a simple tutorial on how to fill this at some point.
    """
    model_name = models.CharField(max_length=255, blank=False, null=False)
    common_name = models.CharField(max_length=30, blank=False, null=False)
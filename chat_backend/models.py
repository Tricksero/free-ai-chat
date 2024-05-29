import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model

# Create your models here.
class Todo(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=1024)

# some predefined states questions can have
GENERATION_STATES = [
    ("new", _("new")), # should indicate that this object was newly created and has an empty response
    ("finished", _("finished")), # answer generation complete, polling can be stopped
    ("unfinished", _("unfinished")), # answer generation incomplete, either polling still in progress or interrupted
    ("failed", _("failed")), # indicates that the generation server had an error
]
# some predefined supported api types
GENERATION_STATES = [
    ("gpt4all", _("gpt4all")), # should indicate that this object was newly created and has an empty response
    ("ollama", _("ollama")), # answer generation complete, polling can be stopped
]

class Question(models.Model):
    """
    Model that saves all data about a question-answer interaction in a format that
    can easily be used to display a chat log in the frontend.
    TODO: Look how the models expect logs to be passed onto them and provide serializers.
    """
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, default="", null=False, blank=False)
    question = models.CharField(max_length=255, null=False, blank=False)
    #model = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, default="new", choices=GENERATION_STATES, blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question

class Conversation(models.Model):
    """
    Model that saves basic information about a conversation to be displayed in a list to the left.
    """
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255, default="New Conversation Started!", null=False, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)

class LanguageModel(models.Model):
    """
    Names of models available to chat with.
    TODO: Maybe use fixtures, APIs or create a simple tutorial on how to fill this at some point.
    """
    model_name = models.CharField(max_length=255, blank=False, null=False)
    common_name = models.CharField(max_length=30, blank=False, null=False)
    #api = models.ForeignKey("Model_API", on_delete=models.CASCADE)

    def __str__(self):
        return self.common_name

#class Supported_API_Type(models.Model):
    #"""
    #API Types may be added in a modular design enabling users to write
    #Plugins that add custom API Types that completely alter the way messages
    #are generated and may provide support to APIs that have not been forseen
    #to be added. Though this is in the far future.
    #"""
    #id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    #name = models.CharField(max_length=30, blank=False, null=False, unique=True)

class Model_API(models.Model):
    """
    To make integration of different model APIs easier and to provide support for diffrent kinds of apis
    models should also be bound to one api which is then assigned a connection type i.e. tcp, https
    """
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    common_name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    port = models.PositiveIntegerField(_("port"), blank=True, null=True, validators=[
        MaxValueValidator(65535)
        ])
    uri = models.CharField(max_length=255, blank=True, null=True)
    #type = models.ForeignKey("Supported_API_Type", on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default="gpt4all", choices=GENERATION_STATES, blank=False, null=False)

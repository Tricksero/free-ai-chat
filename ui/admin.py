from django.contrib import admin
from ui.models import Question, Conversation, LanguageModel

for model in [
    Question,
    Conversation,
    LanguageModel
    ]:
    admin.site.register(model)
# Register your models here.

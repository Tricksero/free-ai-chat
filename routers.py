# ./routers.py

from rest_framework import routers
from django.urls import re_path, path

from chat_backend.views import regular_pull, new_question, index, room
from chat_backend.viewsets import TodoViewSet, QuestionViewSet, ConversationViewSet

from chat_backend import consumers

router = routers.SimpleRouter()

# DRF api endpoints
router.register(r'todo', TodoViewSet, basename="todo")
router.register(r'question', QuestionViewSet, basename="question")
router.register(r'conversation', ConversationViewSet, basename="conversion")

# create question and pull answer
#router.register(r'new_question', new_question, basename="new_question")
#router.register(r'pull-question/<id>', regular_pull, basename="regular_pull")

urlpatterns = router.urls

urlpatterns += [
    path("", index, name="index"),
    path("<str:room_name>/", room, name="room"),
]

websocket_urlpatterns = [
    re_path(r"ws/api/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
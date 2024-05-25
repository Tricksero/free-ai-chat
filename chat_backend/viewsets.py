from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from chat_backend.models import Todo

from chat_backend.serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [AllowAny]
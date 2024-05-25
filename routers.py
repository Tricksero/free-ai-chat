# ./routers.py

from rest_framework import routers

from chat_backend.viewsets import TodoViewSet

router = routers.SimpleRouter()

router.register(r'todo', TodoViewSet, basename="todo")

urlpatterns = router.urls
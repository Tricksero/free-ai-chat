from rest_framework import serializers

from chat_backend.models import Todo


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['name', 'desc']
        read_only_fields = ['id']
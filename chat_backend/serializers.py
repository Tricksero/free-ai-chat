from rest_framework import serializers

from chat_backend.models import Todo, Question, Conversation


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['name', 'desc']
        read_only_fields = ['id']

class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ['title', 'date']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['answer', 'question', 'state', 'date']
        read_only_fields = ['id']


from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from util.zmq_client import send_question
from chat_backend.models import Question, Conversation
from django.http import JsonResponse
from chat_backend.serializers import QuestionSerializer

def pull_answer(question_obj):
    resp, state = send_question(question_obj.question, question_obj.id)
    question_obj.answer = resp
    question_obj.state = state
    question_obj.save()
    return question_obj

# Create your views here.
@require_http_methods(["POST", "OPTIONS"])
def new_question(request):
    """
    View for generating a new question response, returns answer text as response.
    """
    conv_id = request.post.get("conversation_id")
    question_text = request.post.get("question")

    # maybe get conversation log to pass to gpt4all
    conv_obj = Conversation.objects.get(id=conv_id)

    question_obj = Question.objects.create(
        conversation=conv_obj,
        question=question_text
    )
    question_obj = pull_answer(question_obj)

    question_json = QuestionSerializer(instance=question_obj)
    print("first pull: ", question_json)
    return JsonResponse(data=question_json)



@require_http_methods(["GET", "OPTIONS"])
def regular_pull(request, id):
    """
    View for generating a new question response, returns answer text as response.
    """
    question_obj = Question.objects.get(id=id)

    question_obj = pull_answer(question_obj)

    question_json = QuestionSerializer(instance=question_obj)
    print("regular pull: ", question_json)
    return JsonResponse(data=question_json)


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
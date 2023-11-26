import time
import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Question, Conversation
from util.zmq_client import send_question
from ui.forms import QuestionForm

DEFAULT_CHAT_MODEL_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"
DEFAULT_TIMEOUT = 100000  

# utility
def question_json_response(question_obj, new_text):
    question_obj
    context = {
        "id": str(question_obj.id),
        "question": question_obj.question,
        "answer": new_text,
        "state": question_obj.state,
    }
    return JsonResponse(context)

def pull_answer(request, question_id):
    """
    Partial view for displaying a question, expecting a post with a conversation id and a question id

    for quick slowly building responses, messages should be generated word by word and returned
    """
    if request.method == "POST":
        question_obj = Question.objects.get(id=question_id)
        question_json = json.loads(question_obj.json)
        #try:
        new_msg_part, state = send_question(question=question_obj)
        print("new_msg", new_msg_part)
        #except Exception as e:
            #print("new question could not be generated ", e)
            #question_obj.state = "failed"
            #return HttpResponse("failed")
            
        question_obj.state = state
        old_msg_parts = question_obj.answer
        question_obj.answer = old_msg_parts + "".join(new_msg_part)

        #question_obj.json = json.dumps(question_json)
        question_obj.save()

        return question_obj, "".join(new_msg_part)

# main views
@login_required
def home_view(request):
    context = {}
    return render(request, "home.html", context=context)

@login_required
def chat_view(request):
    context = {
        "model": "",
        "chats": [],
        "form": QuestionForm,
    }
    print("chat_object", request.session.get("model"))

    return render(request, "chat.html", context=context)

# htmx
#def question_input(request):
    #if request.method == "POST":
        #context = {
            #"form": QuestionForm
        #}
        #return render(request, "htmx/question_input.html", context=context)

@login_required
def chat_conversation_log(request):
    """
    partial view for conversation log of past answers and questions
    """
    if request.method == "POST":
        conversation_id = request.POST.get("conversation")
        context = {
            "conversation_log": [],
        }
        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id)
        else: 
            conversation = Conversation.objects.all().order_by('-date').first()
            if not conversation:
                return render(request, "htmx/chat_conversation_log.html", context=context)
        request.session["conversation"] = str(conversation.id)
        question_objs = Question.objects.filter(conversation=conversation)
        print("questions", question_objs)
        #print("CONVERSATION:", conversation.id)
        for question_obj in question_objs:
            conversation_pair = {
                "question_id": str(question_obj.id),
                "answer": question_obj.answer,
                "question": question_obj.question,
                "state": question_obj.state,
            }
            context["conversation_log"].append(conversation_pair)
        #print("context", context)
        return render(request, "htmx/chat_conversation_log.html", context=context)

@login_required
def new_or_edit_question(request):
    """
    Partial view for editing or creating a new question, 
    Extends the pull_answer view by handling the creation of a new question
    object or deleting the answer of an old one.
    """
    if request.method == "POST":
        print("post", request.POST)
        #new_question = request.POST.get("new_question")
        question_text = request.POST.get("question_text")
        question_id = request.POST.get("question_id")
        print("question_id", question_id)
        if question_id:
            question_obj = Question.objects.get(id=question_id)
            question_json = json.loads(question_obj.json)
        else:
            conversation_id = request.session.get("conversation")
            print("conversion", uuid.UUID(conversation_id))
            conversation_obj = Conversation.objects.get(id=uuid.UUID(conversation_id))
            if not conversation_obj:
                return
            question_obj = Question.objects.create(conversation=conversation_obj, json="{}")
            question_json = {}

        question_obj.question = question_text
        question_obj.answer = ""
        question_obj.json = json.dumps(question_json)
        question_obj.save()
        print(question_obj.__dict__)
        question_obj, new_text = pull_answer(request, question_obj.id)
        return question_json_response(question_obj, new_text)

@login_required
def regular_pull(request):
    question_id = request.POST.get("question_id")
    question_obj, new_text = pull_answer(request, question_id)
    return question_json_response(question_obj, new_text)
    
        
@login_required
def get_question(request):
    """
    Partial view rendering a single question with response.
    """
    if request.method == "POST":
        print("POST", request.POST)
        question_id = request.POST.get("question")
        conversation_id = request.session.get("conversation")
        conversation_obj = Conversation.objects.get(id=uuid.UUID(conversation_id))
        question_obj = Question.objects.get(
            conversation=conversation_obj.id,
            id=uuid.UUID(question_id),
            )
        context = {
            "answer": question_obj.answer,
            "question": question_obj.question,
        }
        return render(request, "htmx/question.html", context=context)

@login_required
def conversation_list(request):
    """
    Partial view for displaying a list of conversations
    """
    if request.method == "POST":
        #conversations = Conversation.objects.filter("")
        conversations = Conversation.objects.all()
        print("conversations: ", conversations)
        if len(conversations) == 0:
            conversation = Conversation.objects.create()
            conversation.title = "new chat"
            conversations = [conversation]
        context = {
            "conversation_list": [conversations],
        }
        return render(request, "htmx/conversation_list.html", context=context)

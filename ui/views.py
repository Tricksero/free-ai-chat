import time
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ui.models import Question, Conversation
from util.zmq_client import send_question
from ui.forms import QuestionForm

DEFAULT_CHAT_MODEL_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"
DEFAULT_TIMEOUT = 100000  

# utility
def pull_answer(request):
    """
    Partial view for displaying a question, expecting a post with a conversation id and a question id

    for quick slowly building responses, messages should be generated word by word and returned
    """
    if request.method == "POST":
        question_id = request.POST.get("question")
        question_obj = Question.get(id=question_id)

        try:
            new_msg_part, finished = send_question(id=question_id)
        except Exception as e:
            print("new question could not be generated ", e)
            question_obj.state = "failed"
            return question_obj
            
        if finished:
            question_json.state = "finished"
        question_json = json.loads(question_obj.json)
        old_msg_parts = question_json["answer"]
        question_json["answer"] = old_msg_parts + "".join(new_msg_part)

        question_obj.json = json.dumps(question_json)
        question_obj.save()

        return question_obj

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
    partial view for conversation log
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
        question_objs = Question.objects.filter(conversation=conversation)
        for question_obj in question_objs:
            conversation = {
                "question_id": question_obj.id,
            }
            context["conversation_log"].append(conversation)
        return render(request, "htmx/chat_conversation_log.html", context=context)

@login_required
def new_or_edit_question(request):
    """
    Partial view for editing or creating a new question, 
    Extends the pull_answer view by handling the creation of a new question
    object or deleting the answer of an old one.
    """
    if request.method == "POST":
        new_question = request.POST.get("new_question")
        question_id = request.POST.get("question")
        if question_id:
            question_obj = Question.get(id=question_id)
            question_json = json.loads(question_obj.json)
        else:
            conversation_id = request.POST.get("conversation")
            conversation_obj = Conversation.get(id=conversation_id)
            if not conversation_obj:
                return
            question_obj = Question.create(id=question_id,
                                        conversation=conversation_id
                                        )
            question_json = {}

        question_json["question"] = new_question
        question_json["answer"] = ""
        question_obj.json = json.dumps(question_json)
        question_json.state = "unfinished"
        return pull_answer(request)



@login_required
def regular_pull(request):
    question_obj = pull_answer(request)
    context = {
        "question": question_obj,
    }
    return render(request, "htmx/question.html", context=context)
    
        
@login_required
def get_question(request):
    """
    Partial view rendering a single question with response.
    """
    if request.method == "POST":
        question_id = request.POST.get("question")
        conversation_id = request.POST.get("conversation")
        conversation_obj = Conversation.get(id=conversation_id)
        question_obj = Question.get(
            conversation=conversation_obj.id,
            id=question_id,
            )
        context = {
            "question": question_obj
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

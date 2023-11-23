import time
import json
import uuid
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Question, Conversation
from util.zmq_client import send_question
from ui.forms import QuestionForm

DEFAULT_CHAT_MODEL_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"
DEFAULT_TIMEOUT = 100000  

# utility
def pull_answer(request, question_id):
    """
    Partial view for displaying a question, expecting a post with a conversation id and a question id

    for quick slowly building responses, messages should be generated word by word and returned
    """
    if request.method == "POST":
        question_obj = Question.objects.get(id=question_id)
        question_json = json.loads(question_obj.json)
        try:
            new_msg_part, finished = send_question(id=str(question_id), question=question_json["question"])
            print("new_msg", new_msg_part)
        except Exception as e:
            print("new question could not be generated ", e)
            question_obj.state = "failed"
            return HttpResponse("failed")
            
        if finished:
            question_json.state = "finished"
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
        question_objs = Question.objects.filter(conversation=conversation)
        #print("CONVERSATION:", conversation.id)
        request.session["conversation"] = str(conversation.id)
        for question_obj in question_objs:
            try:
                question_json = json.loads(question_obj.json)
                print("json", question_json)
                answer = question_json.get("answer"),
                question = question_json.get("question"),
                conversation = {
                    "question_id": question_obj.id,
                    "answer": answer,
                    "question": question,
                }
            except Exception as e:
                print("could not decode", e)
                continue
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

        question_json["question"] = question_text
        question_json["answer"] = ""
        question_obj.json = json.dumps(question_json)
        question_obj.state = "unfinished"
        print(question_obj.__dict__)
        return pull_answer(request, question_obj.id)



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
        conversation_obj = Conversation.objects.get(id=conversation_id)
        question_obj = Question.objects.get(
            conversation=conversation_obj.id,
            id=question_id,
            )
        json_dict = json.loads(question_obj.json)
        question = json_dict["question"]
        answer = json_dict["answer"]
        context = {
            "answer": answer,
            "question": question,
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

import json
import uuid
from dal import autocomplete
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Question, Conversation
from util.zmq_client import send_question
from ui.forms import QuestionForm, ModelSelectForm
from ui.models import LanguageModel
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
        # in case someone tries to pull maliciously to retrieve answer text of messages of other users
        if not question_obj.conversation.user == request.user:
            raise PermissionDenied("You don't have permission to access this question.")

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

# buttons
@login_required
def change_conversation(request):
    """
    Set conversation for this session and reload the chat page.
    """
    conversation = request.POST.get("conversation")
    if Conversation.objects.filter(id=conversation, user=request.user).exists():
        request.session["conversation"] = conversation
    else:
        print("attempt to access unaccessable conversation: ", conversation)
    #return redirect(reverse("user_interface:chat"))
    return HttpResponse(200)

@login_required
def create_conversation(request):
    """
    Set conversation for this session and reload the chat page.
    """
    conversation = Conversation.objects.create(user=request.user)
    request.session["conversation"] = str(conversation.id)
    return HttpResponse(200)
    #return redirect(reverse("user_interface:chat"))

@login_required
def change_model(request):
    """
    Set conversation for this session, there should be no reloading necessary.
    If there is a new question asked the selected bot will answer. Preferably
    with the given log as context for the conversation.
    """
    model_id = request.POST.get("model")
    model = LanguageModel.objects.filter(id=model_id)
    if model.exists():
        request.session["model_name"] = model_id
    else:
        print("attempt to access unaccessable model: ", model_id)
    return HttpResponse(200)

# main views
@login_required
def home_view(request):
    context = {}
    return render(request, "home.html", context=context)

@login_required
def chat_view(request):
    # set session variables
    print("CONVERSATION SESSION: ", request.session.get("conversation"))
    if not request.session.get("conversation"):
        conversation_id = str(Conversation.objects.filter(user=request.user).latest("date").id)
        if not conversation_id:
            conversation_id = Conversation.objects.create(user=request.user).id

        request.session["conversation"] = conversation_id
    # TODO: should pick model last used for the picked conversation by default
    if not request.session.get("model"):
        current_model = LanguageModel.objects.get(model_name=DEFAULT_CHAT_MODEL_NAME)
        request.session["model"] = str(current_model.id)
    else:
        current_model = LanguageModel.objects.get(id=request.session.get("model"))

    model_select = ModelSelectForm(initial={"model_name": current_model})
    print("conversation", request.session.get("conversation"))
    chat_forms = {
       "QuestionForm": QuestionForm,
       "ModelSelectForm": model_select,
    }
    context = {
        "model": current_model,
        "chats": [],
        "forms": chat_forms,
        "hide_navbar": True,
        "dal_media": autocomplete.Select2().media,
    }
    print("chat_object", request.session.get("model"))

    return render(request, "chat.html", context=context)

# htmx
@login_required
def chat_conversation_log(request):
    """
    partial view for conversation log of past answers and questions
    """
    if request.method == "POST":
        conversation_id = request.POST.get("conversation")
        if not conversation_id:
            conversation_id = request.session.get("conversation", None)
        page_num = request.POST.get("page")
        context = {
            "conversation_log": [],
        }
        # gets conversation object defaults to the newest
        if conversation_id:
            #print("CONVERSATION:", conversation.id)
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.filter(user=request.user).order_by('-date').first()
            # if there are no conversations just show an emty list
            if not conversation:
                return render(request, "htmx/chat_conversation_log.html", context=context)

        # get all questions for the current conversation starting with the newest
        request.session["conversation"] = str(conversation.id)
        question_objs = Question.objects.filter(conversation=conversation).order_by("-date")
        print("questions", question_objs)
        # serialize the question into an object displayed by the frontend
        # TODO: Maybe define a proper serializer for this.
        conversation_pair_list = []
        for question_obj in question_objs:
            conversation_pair = {
                "question_id": str(question_obj.id),
                "answer": question_obj.answer,
                "question": question_obj.question,
                "state": question_obj.state,
            }
            conversation_pair_list.append(conversation_pair)
        # paginate the questions so not all of them are passed to the frontend
        conversation_paginator = Paginator(conversation_pair_list, 10)
        conversation_pair_page = conversation_paginator.get_page(page_num)
        context["conversation_log"] = conversation_pair_page
        #print(f"CONVERSATION PAGE: {conversation_pair_page}")

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
        question_text = request.POST.get("question_text")
        question_id = request.POST.get("question_id")
        print("question_id", question_id)
        if question_id:
            question_obj = Question.objects.get(id=question_id)
            question_json = json.loads(question_obj.json)
        else:
            conversation_id = request.session.get("conversation")
            print("conversion", uuid.UUID(conversation_id))
            conversation_obj = Conversation.objects.get(id=uuid.UUID(conversation_id), user=request.user)
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
    """
    Retrieves the next part of an answer util it is finished.
    """
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
        conversation_obj = Conversation.objects.get(id=uuid.UUID(conversation_id), user=request.user)
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
    TODO: Make this user specific.
    """
    if request.method == "POST":
        conversation_id = request.POST.get("conversation")
        if not conversation_id:
            conversation_id = request.session.get("conversation")
        # get all conversations or create a new one if none is saved
        #conversations = Conversation.objects.filter("")
        conversations = Conversation.objects.filter(user=request.user)
        print("conversations: ", conversations)

        # in the frontend we want to display the date of the past conversations relative to the
        # current date unless it was longer than one year ago, this is much like how chatgpt does
        # it right now
        now = timezone.now()
        conversations_date_dict = {}
        for conversation in conversations.order_by("-date"):
            date_string = ""
            absolute_date = conversation.date
            if not now.year == absolute_date.year:
                date_string = absolute_date.strftime("%Y")
            else:
                time_passed = now - absolute_date
                match (time_passed.days):
                    case n if n<1:
                        date_string = _("Today")
                    case n if n<2:
                        date_string = _("Yesterday")
                    case n if n<7:
                        date_string = _("This Week")
                    case n if n<14:
                        date_string = _("Last Week")
                    case n if n<30:
                        date_string = _("Last 30 Days")
                    case _:
                        date_string = absolute_date.strftime("%B")

            if not conversations_date_dict.get(date_string):
                conversations_date_dict[date_string] = []
            conversations_date_dict[date_string].append(conversation)

        context = {
            "conversation_list": conversations_date_dict,
            "selected_conversation": conversation_id,
        }
        return render(request, "htmx/conversation_list.html", context=context)

# dal
class DAL_Model_Name(autocomplete.Select2QuerySetView):
    model = LanguageModel
    def get_queryset(self):
        qs = LanguageModel.objects.all()

        if self.q:
            qs = qs.filter(common_name=self.q)

        return qs

    def get_result_label(self, obj):
        return obj.common_name

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ui.models import Question, Conversation

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
    }
    return render(request, "chat.html", context=context)

# htmx
@login_required
def chat_conversation_log(request):
    """
    partial view for conversation log
    """
    context = {
        "conversation_log": [],
    }
    for i in range(3):
        conversation = {
            "question": "how do you do",
            "answer": f"fine{i}"
        }
        context["conversation_log"].append(conversation)
    return render(request, "htmx/chat_conversation_log.html", context=context)

@login_required
def question(request):
    """
    partial view for displaying a question, expecting a post with a conversation id and a question id
    """
    if request.method == "POST":
        question_id = request.POST.get("question")
        conversation_id = request.POST.get("conversation")
        conversation_obj = Conversation.get(id=conversation_id)
        question_obj = Question.filter(
            conversation=conversation_obj.id,
            id=question_obj,
            )
        print("questions: ", question_obj.__dict__)
        question = {
            "question": "",
            "answer": ""
        }
        context = {
            "question": question
        }
        return render(request, "htmx/question.html", context=context)

@login_required
def conversation_list(request):
    """
    partial view for displaying a list of conversations
    """
    if request.method == "POST":
        context = {
            "conversation_list": [],
        }
        return render(request, "htmx/conversation_list.html", context=context)
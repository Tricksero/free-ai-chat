from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# main views
@login_required
def home_view(request):
    context = {}
    return render(request, "base.html", context=context)

@login_required
def chat_view(request):
    context = {
        "model": "",
        "chats": [],
    }
    return render(request, "chat.html", context=context)

# htmx
@login_required
def chat_body(request):
    context = {
        "questions": [],
    }
    return render(request, "chat_body.html", context=context)

@login_required
def question(request):
    question = {}
    context = {
        "question": question
    }
    return render(request, "question.html", context=context)

@login_required
def conversation_list(request):
    if request.method == "POST":
        context = {
            "conversations": [],
        }
        return render(request, "conversation_list.html", context=context)
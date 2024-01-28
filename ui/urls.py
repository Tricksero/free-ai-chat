#from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('chat/', views.chat_view, name="chat"),

    # htmx
    path('chat-conversation-log/', views.chat_conversation_log, name="chat-conversation-log"),
    path('question/', views.get_question, name="chat-question"),
    path('conversation-list/', views.conversation_list, name="chat-conversation-list"),
    path('new_edit_question/', views.new_or_edit_question, name="question-new-edit"),
    # ajax
    path('regular_pull/', views.regular_pull, name="regular-pull"),
    path('change_conversation', views.change_conversation, name="change-conversation"),
    path('create_conversation', views.create_conversation, name="create-conversation"),
    path('change_model', views.change_model, name="change-model_name"),
    # dal
    re_path(r'^model_name-autocomplete/$', views.DAL_Model_Name.as_view(), name='model_name-autocomplete'),
]
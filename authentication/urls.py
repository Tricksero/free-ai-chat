from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserLoginForm
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(
        "login",
        LoginView.as_view(
            template_name="auth/login.html",
            authentication_form=UserLoginForm,
        ),
        name="login",
    ),
    path(
        "logout",
        LogoutView.as_view(
            template_name="auth/logout.html",
        ),
        name="logout",
    ),
]

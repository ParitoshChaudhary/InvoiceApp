from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}")
    context = {}
    return render(request, "users/register.html", context)

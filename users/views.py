from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm
from .models import UserAccount
from django.conf import settings


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}")
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('home')

        else:
            context['registration_form'] = form
    return render(request, "users/register.html", context)


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context["login_form"] = form
    return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
        return redirect


def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = UserAccount.objects.get(pk=user_id)
    except UserAccount.DoesNotExist:
        return HttpResponse("Something went wrong. Please try later")
    if account:
        context['id'] = account.id
        context['email'] = account.email
        context['username'] = account.username
        context['profile_pic'] = account.profile_pic.url
        context['company_name'] = account.company_name

        is_self = True
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['BASE_URL'] = settings.BASE_URL

    return render(request, 'users/account.html', context)


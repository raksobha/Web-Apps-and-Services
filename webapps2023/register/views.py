from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from register.forms import RegisterForm


@csrf_protect
def signup_user(request):
    if request.method == "POST":
        signup_form = RegisterForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get("username")
            email = signup_form.cleaned_data.get("email")
            password = signup_form.cleaned_data.get("password1")
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    signup_form.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    messages.success(request, "Registration successful. Logging in...")
                    return render(request, "main/home.html")
                else:
                    messages.error(request, "Account with that email already exists")
            else:
                messages.error(request, "Username is already in use")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    signup_form = RegisterForm()
    return render(request, "register/signup.html", {"signup_user": signup_form})


@csrf_protect
def login_user(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return render(request, "main/home.html")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    login_form = AuthenticationForm()
    return render(request, "register/login.html", {"login_user": login_form})


@csrf_protect
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

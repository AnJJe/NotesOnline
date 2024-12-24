# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, EditUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.contrib.auth import logout


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не выполняем немедленное сохранение объекта в БД
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            # is_admin = form.cleaned_data.get('is_admin', False)
            # if is_admin:
            user_profile = user.userprofile
            user_profile.is_admin = True
            user_profile.save()
            messages.success(request, 'Account created successfully! You can now log in')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid login details provided.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='login')
def home(request):
    return redirect('notes:input')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')


@login_required
def edit_user(request):
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile information has changed")
            return redirect("profile")
    else:
        form = EditUserForm(instance=request.user)
    return render(request, "users/edit_user.html", {"form": form})

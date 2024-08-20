from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.user.is_authenticated:
        return redirect('register_company')
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        users = User.objects.get(username=username)

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('register')
        
        if len(password) < 6:
            messages.add_message(request, constants.ERROR, 'A senha precisa ter ao menos 6 digitos')
            return redirect('register')


        if users.exists():
            messages.add_message(request, constants.ERROR, 'Esse usuário já existe')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            password=password
        )
        return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('register_company')

    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('register_company')
        messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos")
        return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
    

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User

def login(request): 
    return render(request, 'accounts/login.html')

def logout(request): 
    return render(request, 'accounts/logout.html')

def cadastro(request): 
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    usuario = request.POST.get('usuario')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not senha or not senha2 or not usuario:
        messages.error(request, 'Nenhum campo foi preenchido.')
        return render(request, 'accounts/cadastro.html')
    
    if len(senha) < 6:
        messages.error(request, 'O campo senha precisa ter no mínimo 6 caracteres!')
        return render(request, 'accounts/cadastro.html')
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/cadastro.html')

    if len(nome) < 2:
        messages.error(request, 'O campo nome precisa ter no mínimo 2 caracteres!')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.error(request, 'As senhas não conferem')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email = email):
        messages.error(request, 'O email já existe')
        return render(request, 'accounts/cadastro.html')
    messages.success(request, 'Registrado com Sucesso!')

    user = User.objects.create_user(username=usuario,
                                    email=email,
                                    password = senha,
                                    first_name = nome,
                                    last_name=sobrenome)
    user.save()

    return redirect('login')

def dashboard(request): 
    return render(request, 'accounts/dashboard.html')

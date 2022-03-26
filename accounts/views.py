from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

def login(request): 
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password = senha)
    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso')
        return redirect('dashboard')

def logout(request): 
    auth.logout(request)
    return redirect('dashboard')

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

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':            
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form })
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário')
        return render(request, 'accounts/dashboard.html', {'form': form })
    
    nome = request.POST.get('nome')
    
    if len(nome) < 5:
        messages.error(request, 'Descrição precisa ter mais do que 5 caracteres')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form })
    form.save()
    messages.success(request, f"Contato {request.POST.get('nome')} salvo com sucesso")

    return redirect('dashboard')
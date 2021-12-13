from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.shortcuts import get_object_or_404, redirect, render
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Simplemooc.accounts.models import PasswordReset
from Simplemooc.accounts.utils import generate_hash_key
from .forms import EditAccountForm, RegisterForm, ResetPassword
from django.conf import settings

User = get_user_model()

@login_required #Redireciona para o login se não houver usuário logado
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)

def register(request):
    template_name = 'accounts/register.html'

    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = RegisterForm(request.POST) #Utiliza do form custom com email
        if form.is_valid(): #Verifica se o form é valido
            user = form.save() #Salva os dados em um objeto da tabela

            # Esse trecho da conflito com um model personalizado para usuário, ao invés disso, var direto para login
            '''user = authenticate(
                username = user.username, password = form.cleaned_data['password1']
            )#Autentica o usuário'''
            
            login(request, user)#Automaticamente loga o usuário após o cadastro
            return redirect('core:home') #Redireciona para a página inicial
    else:
        #form = UserCreationForm()
        form = RegisterForm() 

    context = {
        'form' : form #Classe simples de criação de usuários do Django
    }

    return render(request, template_name, context)

def reset_password(request):
    template_name = 'accounts/reset.html'
    context = {}
    form = ResetPassword(request.POST or None) # Mesma coisa que os outros, só que com menos linhas
    if form.is_valid():
        form.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, template_name, context)

def reset_password_confirm(request, key):
    template_name = 'accounts/confirm_reset.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key = key) # Verifica se há uma solicitação existente
    form = SetPasswordForm(user=reset.user, data=request.POST or None) # Utiliza do form padrão do Django para resetar senha
    if form.is_valid():
        form.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance = request.user)
            messages.success(request,'Dados da conta alterados com sucesso')
    
    else:
        form = EditAccountForm(instance = request.user)

    context['form'] = form

    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}

    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso')

    else:
        form = PasswordChangeForm(user=request.user)
    
    context['form'] = form

    return render(request, template_name, context)
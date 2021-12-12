from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.translation import templatize
from .forms import EditAccountForm, RegisterForm
from django.conf import settings

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
            user = authenticate(
                username = user.username, password = form.cleaned_data['password1']
            )#Autentica o usuário
            login(request, user)#Automaticamente loga o usuário após o cadastro
            return redirect('core:home') #Redireciona para a página inicial
    else:
        #form = UserCreationForm()
        form = RegisterForm() 

    context = {
        'form' : form #Classe simples de criação de usuários do Django
    }

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
            context['sucess'] = True
    
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
            context['sucess'] = True

    else:
        form = PasswordChangeForm(user=request.user)
    
    context['form'] = form

    return render(request, template_name, context)
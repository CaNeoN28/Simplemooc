from django.shortcuts import redirect, render
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.conf import settings

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
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

def register(request):
    template_name = 'accounts/register.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): #Verifica se o form é valido
            form.save() #Salva os dados em um objeto da tabela
            return redirect(settings.LOGIN_URL) #Redireciona para a página de Login
    else:
        form = UserCreationForm()

    context = {
        'form' : form #Classe simples de criação de usuários do Django
    }

    return render(request, template_name, context)
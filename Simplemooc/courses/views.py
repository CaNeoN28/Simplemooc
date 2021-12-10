from typing import ContextManager
from django.http import request
from django.shortcuts import get_object_or_404, render

from .models import Course #Referencia a tabela Course do BD
from .forms import ContactCourse #Chamado ao form de contato do app

# Create your views here.

def index(request):
    courses = Course.objects.all() #Possui todos os objetos da tabela Course 
    template_name = 'courses/index.html'

    context = {
        'courses' : courses #Adiciona course ao contexto do template
    }
    return render(request, template_name, context)

'''
def details(request, pk):
    #course = Course.objects.get(pk = pk) #Filtra o curso com o atributo passado (pk), retorna uma exceção desagradável se não houver correspondência
    course = get_object_or_404(Course, pk = pk) #Retorna um 404 se não houver correspondência
    template_name = 'courses/details.html'

    context = {
        'course' : course
    }

    return render(request, template_name, context)'''

def details(request, slug):
    course = get_object_or_404(Course, slug = slug)
    context = {}

    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid(): #Verifica se o formulário foi dvidamente preenchido
            context['is_valid'] = True #Auxiliar para o template

            '''for field in form:
                print(field.label, field.data) #Retorna os valores no terminal'''

            form.send_mail(course)#Método para enviar um email para o terminal
            form = ContactCourse()
    else:
        form = ContactCourse()

    template_name = 'courses/details.html'

    context['forms'] = form
    context['course'] = course

    return render(request, template_name, context)

    
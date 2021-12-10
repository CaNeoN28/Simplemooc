from typing import ContextManager
from django.http import request
from django.shortcuts import render
from .models import Course #Referencia a tabela Course do BD

# Create your views here.

def index(request):
    courses = Course.objects.all() #Possui todos os objetos da tabela Course 
    template_name = 'courses/index.html'

    context = {
        'courses' : courses #Adiciona course ao contexto do template
    }
    return render(request, template_name, context)

def details(request, pk):
    course = Course.objects.get(pk = pk) #Filtra o curso com o atributo passado (pk)
    template_name = 'courses/details.html'

    context = {
        'course' : course
    }

    return render(request, template_name, context)

    
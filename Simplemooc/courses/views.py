from typing import ContextManager
from django.http import request
from django.shortcuts import render
from .models import Course #Referencia a tabela Course do BD

# Create your views here.

def index(request):
    course = Course.objects.all() #Possui todos os objetos da tabela Course 
    template_name = 'courses/index.html'

    context = {
        'course' : course #Adiciona course ao contexto do template
    }
    return render(request, template_name, context)
    
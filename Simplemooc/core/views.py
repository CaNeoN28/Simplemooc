from django import http
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    template_name = 'home.html',
    return render(request, template_name) #retorna o template e seu conteúdo

def contact(request):
    template_name = 'contact.html'
    return render(request, template_name)
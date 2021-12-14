from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
   #path('<int:pk>', views.details, name = 'details') #regular expression para receber uma url com base na pk de um curso
    path('<slug:slug>', views.details, name = 'details'),
    path('<slug:slug>/inscricao', views.enrollments, name='enrollment'),
    path('<slug:slug>/anuncios', views.announcements, name='announcements'),
    path('<slug:slug>/cancelar-inscricao', views.undo_enrollment, name = 'undo-enrollment')
]
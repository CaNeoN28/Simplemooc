from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar/', LoginView.as_view(template_name = 'accounts/login.html', next_page = None), name = 'login'),
    #A classe LoginView deve ser passada com o método .asView()
    #O método deverá ter atributos para um template customizado
    path('sair', LogoutView.as_view(next_page = 'core:home'), name = 'logout'),
    #Mesmo que o anterior, mas não possui um template, apenas redireciona
    path('cadastro/', views.register, name='register'),
    path('editar/', views.edit, name='edit')
]
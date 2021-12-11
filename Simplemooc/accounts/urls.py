from django.contrib.auth.views import LoginView
from django.urls import path

urlpatterns = [
    path('entrar/', LoginView.as_view(template_name = 'accounts/login.html', next_page = None), name = 'login')
    #A classe LoginView deve ser passada com o método .asView()
    #O método deverá ter atributos para um template customizado
]
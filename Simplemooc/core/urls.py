from django.urls import path
from . import views #importa as views de core com o nome core_views(organização)

urlpatterns = (
    path('início/', views.home, name='home'), #chama a view home de core no caminho vazio
    path('contato/', views.contact, name='contact')
)

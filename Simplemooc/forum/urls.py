from django.contrib.auth.views import LoginView, LogoutView
from . import views as forum_views
from django.urls import path

urlpatterns = [
    path('', forum_views.index, name='index'),
    path(r'tag/<tag>', forum_views.index, name='index_tagged'),
    path(r'topico/<slug:slug>', forum_views.thread, name='thread'),
    path(r'respostas/<int:pk>/correta', forum_views.reply_correct, name='reply-correct'),
    path(r'respostas/<int:pk>/incorreta', forum_views.reply_incorrect, name='reply-incorrect'),
]
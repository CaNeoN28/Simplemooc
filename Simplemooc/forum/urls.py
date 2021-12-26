from django.contrib.auth.views import LoginView, LogoutView
from . import views as forum_views
from django.urls import path

urlpatterns = [
    path('', forum_views.index, name='index'),
    path(r'tag/<tag>', forum_views.index, name='index_tagged'),
    path(r'topico/<slug:slug>', forum_views.thread, name='thread')
]
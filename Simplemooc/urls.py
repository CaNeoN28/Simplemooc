"""Simplemooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from .core import urls as core_urls
from .courses import urls as course_urls
from .accounts import urls as accounts_urls
from .forum import urls as forum_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'', include((core_urls, 'core'), namespace = 'core')),
    path(r'cursos/', include((course_urls, 'courses'), namespace = 'courses')),
    path(r'conta/', include((accounts_urls, 'accounts'), namespace = 'accounts')),
    path(r'forum/', include((forum_urls, 'forum'), namespace = 'forum'))
]

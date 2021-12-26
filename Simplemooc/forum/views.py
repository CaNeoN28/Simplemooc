from typing import Any
from django.db.models import query
from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView
from taggit.models import Tag

from Simplemooc.forum.models import Thread

# Create your views here.

'''class ForumView(View):
    # template_name = 'forum/index.html'
    def get(self, requests, *args, **kwargs):
        return render(self.request, 'forum/index.html')'''

class ForumView(ListView):
    model = Thread
    paginate_by = 2
    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order', '')

        if order == 'views':
            queryset = queryset.order_by('-views')

        elif order == 'answers':
            queryset = queryset.order_by('-answers')

        tag = self.kwargs.get('tag', None) # Pega um parâmetro nomeado do template
        if tag:
            queryset = queryset.filter(tags__slug__in = [tag]) # Filtra os resultados com base na tag
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context

index = ForumView.as_view()

def forumView(request, tag = None):
    template_name = 'forum/index.html'
    context = {}

    context['tags'] = Thread.tags.all()

    posts = Thread.objects.all()

    order = request.GET.get('order', '')

    if order == 'views':
        posts = posts.order_by('views')
    
    elif order == 'answers':
        posts = posts.order_by('answers')

    if tag:
        posts = posts.filter(tags__slug__in = tag)
    
    context['posts'] = posts
    
    return render(request, template_name, context)
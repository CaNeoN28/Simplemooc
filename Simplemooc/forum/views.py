from typing import Any
from django.db.models import query
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View, ListView, DetailView
from taggit.models import Tag

from Simplemooc.forum.models import Thread
from .forms import ReplyForm

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

class ThreadView(DetailView):
    template_name = 'forum/thread.html'
    model = Thread

    def get_context_data(self, **kwargs: Any):
        context =  super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context
    
    def post(self, request, *args:Any, **kwargs:Any):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para enviar respostas')
            return redirect(self.request.path)

        self.object = self.get_object()
        context = self.get_context_data(object = self.object)
        form = context['form']

        if form.is_valid():
            reply = form.save(commit=False) # Preenche os campos sem salvar, não há usuário definido, então
            #é necessário
            reply.author = self.request.user
            reply.thread = self.object
            reply.save()
            messages.success(request, 'Resposta enviada com sucesso')
            context['form'] = ReplyForm()

        return render(request, 'forum/thread.html', context)

index = ForumView.as_view()
thread = ThreadView.as_view()

def forumView(request, slug = None):
    template_name = 'forum/index.html'
    context = {}

    context['tags'] = Thread.tags.all()

    posts = Thread.objects.all()

    order = request.GET.get('order', '')

    if order == 'views':
        posts = posts.order_by('views')
    
    elif order == 'answers':
        posts = posts.order_by('answers')

    if slug:
        posts = posts.filter(tags__slug__in = [slug])
    
    context['posts'] = posts
    
    return render(request, template_name, context)
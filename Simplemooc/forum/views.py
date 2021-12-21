from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from Simplemooc.forum.models import Thread

# Create your views here.

'''class ForumView(View):
    # template_name = 'forum/index.html'
    def get(self, requests, *args, **kwargs):
        return render(self.request, 'forum/index.html')'''

class ForumView(ListView):
    model = Thread
    paginate_by = 10
    template_name = 'forum/index.html'

index = ForumView.as_view()
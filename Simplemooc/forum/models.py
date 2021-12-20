from django.db import models
from django.conf import settings
# Create your models here.

from taggit.managers import TaggableManager

class Thread(models.Model):
    title = models.CharField('Título', max_length=100)
    body = models.TextField('Conteúdo')
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='user_tread', null=True)

    created_at = models.DateTimeField('Criado em ', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank = True)

    tags = TaggableManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['updated_at']

class Reply(models.Model):
    reply = models.TextField('Resposta')
    correct = models.BooleanField('Correto?', blank = True, default=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='user_reply', null=True)

    created_at = models.DateTimeField('Criado em', blank=True, auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', blank=True, auto_now=True)

    def __str__(self):
        return '{0}/{1}'.format(self.author, self.created_at)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = "Respostas"
        ordering = ['-correct', 'updated_at'] # Booleans são organizados de negativo em positivo
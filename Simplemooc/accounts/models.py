import re

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, 
UserManager) # Classe de utilitários 
from django.conf import settings
from Simplemooc.courses.models import Course

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Nome de usuário', max_length=30, unique=True, #O unique = True é necessário
        validators= [RegexValidator(re.compile('^[\w.@+-]+$'), 'O nomes de usuário inserido é inválido')]
    ) 
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nome', max_length=100)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] #Lista com atributos obrigatórios

    def __str__(self): # Retorna um nome para o objeto
        return self.name or self.username
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.name

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class PasswordReset(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
     verbose_name='Usuário') # Chave estrangeira, referenciando o caminho do usuário padrão
    key = models.CharField('Chave', unique=True, max_length=100) # Atributo principal
    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True) 
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.key)
    
    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name = 'Novas Senhas'
        ordering = ['created_at']

class Enrollments(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
        (3, 'Indisponível')
    )

    #Esses dois atributos referenciam as duas classes pai, cursos e usuários
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
    related_name = 'enrollments', verbose_name='Usuário')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, 
    related_name='enrollments', verbose_name='Curso')

    #Inteiro representando opções
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)

    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)
        #Essa instrução define que não podera haver o mesmo usuário inscrito no mesmo curso duas vezes

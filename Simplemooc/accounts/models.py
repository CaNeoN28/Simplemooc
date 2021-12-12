import re
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, 
UserManager) # Classe de utilitários 

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

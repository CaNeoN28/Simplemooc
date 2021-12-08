from enum import auto
from django.db import models

class CourseManager(models.Manager):
    def search(self, query):
        #retorna o curso onde o nome ou a descrição contem a entrada de pesquisa
        return self.get_queryset().filter(
            models.Q(name__icontains=query),
            models.Q(description__icontains=query)
        )

class Course(models.Model):
    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição', blank=True)

    start_date = models.DateField('Data de início', blank=True, null=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Editado em', auto_now=True)

    image = models.ImageField(upload_to = 'courses/images', verbose_name='Imagem', blank=True, null=True)

    objects = CourseManager() #define o método de pesquisa da tabela
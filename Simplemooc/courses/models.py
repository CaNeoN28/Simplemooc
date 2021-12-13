from django.conf import settings
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
    description = models.TextField('Descrição simples', blank=True)
    about = models.TextField('Sobre o curso', blank=True)

    start_date = models.DateField('Data de início', blank=True, null=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Editado em', auto_now=True)

    image = models.ImageField(upload_to = 'courses/images', verbose_name='Imagem', blank=True, null=True)

    objects = CourseManager() #define o método de pesquisa da tabela

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return (self.slug) #retorna o endereço dos cursos dos slugs correspondentes

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

        ordering = ['name']

class Enrollments(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
        (3, 'Indisponível')
    )

    #Esses dois atributos referenciam as duas classes pai, cursos e usuários
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
    related_name = 'enrollments_user', verbose_name='Usuário')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, 
    related_name='enrollments_course', verbose_name='Curso')

    #Inteiro representando opções
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)

    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    def activate(self):
        self.status = 1
        self.save()
    
    def is_approved(self):
        if self.status == 1:
            return True
        return False

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        ordering = ['course']
        unique_together = (('user', 'course'),)
        #Essa instrução define que não podera haver o mesmo usuário inscrito no mesmo curso duas vezes

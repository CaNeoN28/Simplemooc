from django import conf
from django.conf import settings
from django.db import models
from django.utils import timezone

from Simplemooc.core.mail import send_mail_template

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
    
    def release_lessons(self):
        today = timezone.now().date()
        return (self.course_lesson.filter(release_date__gte=today))

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
    course = models.ForeignKey(Course, on_delete=models.RESTRICT, 
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
    
class Announcements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso', 
    related_name='course_announcements')
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['course','-created_at']

class Comments(models.Model):
    announcement = models.ForeignKey(Announcements, on_delete=models.CASCADE, verbose_name='Anúncio',
    related_name='announcements_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário')
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add = True, blank = True)
    updated_at = models.DateTimeField('Atualizado em', auto_now = True, blank = True)

    def __str__(self):
        #return (self.comment[:20] + '...')
        return (self.user.username[:] + ', '+ self.announcement.course.name[:] +', '+ self.announcement.title[:] +', ' + str(self.created_at))

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['announcement','created_at']
    
class Lesson(models.Model):

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank = True)
    number = models.IntegerField('Número (ordem)', blank = True, default=0)
    release_date = models.DateTimeField('Data de lançamento', blank = True, null = True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True, blank = True)

    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name='course_lesson')

    def __str__(self):
        return self.name

    def is_avaible(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date <= today
        return False    
    # Recebe a informação de que a aula foi lançado ou não, comparando a data de lançamento à atual

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']

class Material(models.Model):
    title = models.CharField('Título', max_length=100)
    embedded = models.TextField('Vídeo embedded', blank = True)
    file = models.FileField(upload_to='lessons/materials', blank = True, null=True)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_material')

    def is_embedded(self):
        return(self.embedded)

    def __str__(self):
        return(self.title)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'

def post_save_announcements(instance, created, **kwargs):
    if created: # Verifica se o anúncio foi criado
        subject = instance.title # Recebe o título do anúncio
        context = {
            'announcement' : instance # Salva o anúncio no contexto
        }

        template_name = 'mail/send_announcement.html'
        enrollments = Enrollments.objects.filter(course = instance.course, status=1)
        # Lista com todas as inscrições válidas referentes ao curso

        for enrollment in enrollments: # Varre a lista de alunos no curso
            recipient_list = [enrollment.user.email] # Salva o email do aluno inscrito no curso
            send_mail_template(subject=subject, template_name=template_name, context=context,
            recipient_list=recipient_list) # Envia o email ao aluno
    
models.signals.post_save.connect(post_save_announcements, sender = Announcements,
 dispatch_uid='post_save_announcements')
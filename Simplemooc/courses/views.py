from django import contrib
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import message
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .models import Announcements, Course, Enrollments, Lesson, Material #Referencia a tabela Course do BD
from .forms import CommentForm, ContactCourse #Chamado ao form de contato do app
from .decorators import enrollment_required

# Create your views here.

def index(request):
    courses = Course.objects.all() #Possui todos os objetos da tabela Course 
    template_name = 'courses/index.html'

    context = {
        'courses' : courses #Adiciona course ao contexto do template
    }
    return render(request, template_name, context)

'''
def details(request, pk):
    #course = Course.objects.get(pk = pk) #Filtra o curso com o atributo passado (pk), retorna uma exceção desagradável se não houver correspondência
    course = get_object_or_404(Course, pk = pk) #Retorna um 404 se não houver correspondência
    template_name = 'courses/details.html'

    context = {
        'course' : course
    }

    return render(request, template_name, context)'''

def details(request, slug):
    course = get_object_or_404(Course, slug = slug)
    context = {}

    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid(): #Verifica se o formulário foi dvidamente preenchido
            context['is_valid'] = True #Auxiliar para o template

            '''for field in form:
                print(field.label, field.data) #Retorna os valores no terminal'''

            form.send_mail(course)#Método para enviar um email para o terminal
            form = ContactCourse()
    else:
        form = ContactCourse()

    template_name = 'courses/details.html'

    context['forms'] = form
    context['course'] = course

    return render(request, template_name, context)

@login_required
def enrollments(request, slug):
    course = get_object_or_404(Course, slug = slug) # Verifica se o curso está presente no BD
    enrollment, create = Enrollments.objects.get_or_create(
        user = request.user, course=course
        )
    # A primeira variável cria sempre, a segunda somente se a inscrição foi criado agora
    
    if create:
        enrollment.activate()
        messages.success(request, 'Inscrição realizada com sucesso!')
    # Ativa a inscrição, e informa ao usuário se ela não foi previamente criada
    
    else:
        messages.info(request, 'Você já está inscrito nesse curso')

    return redirect('accounts:dashboard')

@login_required
@enrollment_required
def announcements(request, slug):
    '''
    course = get_object_or_404(Course, slug = slug)

    if not request.user.is_staff: # Verifica se o membro é da equipe antes de tudo
        enrollment = get_object_or_404(Enrollments, user = request.user, course = course)
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('accounts:dashboard')
    '''
    course = request.course # Passa o curso presente no contexto, que no caso, vem pelo decorator @enrollment_required
    template_name = 'courses/announcements.html'
    context = {
        'course' : course,
        'announcements' : course.course_announcements.all()
    }
    
    return render(request, template_name, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course

    announcement = get_object_or_404(course.course_announcements.all(), pk = pk)
    #Pega um anúncio específico de um curso específico, usa o related_name 
    
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'O seu comentário foi enviado com sucesso')

    template_name = 'courses/show_announcement.html'
    context = {
        'course' : course,
        'announcement' : announcement,
        'form' : form,
    }

    return render(request, template_name, context)

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug = slug)
    enrollment = get_object_or_404(Enrollments, course = course, user = request.user)

    if request.method == 'POST': 
        enrollment.delete()
        messages.success(request, 'Inscrição cancelada com sucesso')
        return redirect('accounts:dashboard')
    # A inscrição só é cancelada quando o usuário aperta um botão na página, mas a opção de voltar
    #tem a tag <a></a>

    template_name = 'courses/undo_enrollment.html'
    context = {
        'course' : course,
        'enrollment' : enrollment
    }

    return render(request, template_name, context)

@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template_name = 'courses/lessons.html'
    lessons = course.release_lessons()
    
    if request.user.is_staff:
        lessons = course.course_lesson.all()
        
    context = {
        'course' : course,
        'lessons' : lessons
    }

    return render(request, template_name, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk = pk, course = course)

    if not request.user.is_staff and not lesson.is_avaible():
        messages.error(request, 'Essa aula não está disponivel')
        return redirect('courses:lessons', slug=slug)
    
    template_name = 'courses/lesson.html'
    context = {
        'course' : course,
        'lesson' : lesson
    }

    return render(request, template_name, context)

@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk = pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_avaible():
        messages.error(request, 'Esse material não está disponível')
        return redirect('courses:lesson', slug=slug, pk=pk)
    if not material.is_embedded():
        return redirect(material.file.url)
    template_name= 'courses/material.html'
    context = {
        'course' : course,
        'material' : material,
        'lesson' : lesson
    }

    return render(request, template_name, context)

    
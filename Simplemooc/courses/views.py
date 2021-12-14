from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Announcements, Course, Enrollments #Referencia a tabela Course do BD
from .forms import ContactCourse #Chamado ao form de contato do app

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
def announcements(request, slug):
    course = get_object_or_404(Course, slug = slug)

    if not request.user.is_staff: # Verifica se o membro é da equipe antes de tudo
        enrollment = get_object_or_404(Enrollments, user = request.user, course = course)
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('accounts:dashboard')

    template_name = 'courses/announcements.html'
    context = {
        'course' : course,
        'announcements' : course.course_announcements.all()
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
    

    
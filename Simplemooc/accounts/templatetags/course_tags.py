from django.template import Library

register = Library()

from Simplemooc.courses.models import Enrollments

@register.inclusion_tag('accounts/templatetags/my_course.html') # Pasta do template da tag
def my_courses(user):
    enrollments = Enrollments.objects.filter(user = user) 
    context = {
        'enrollments' : enrollments
    }
    
    return context
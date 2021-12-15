from django.contrib import admin

from .models import Announcements, Comments, Course, Enrollments, Lesson, Material

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'start_date'] #Informações exibidas nas listas de cursos
    search_fields = ['name', 'slug'] #Define os espaços onde pesquisar 

    prepopulated_fields = {'slug' : ('name',)} #Recomenda automaticamente um atalho com base no nome do curso
                                               #OBS : A vírgula é estritamente necessária, caso contrário não será reconhecido uma lista

admin.site.register(Course, CourseAdmin) #Possibilita a alteração dos cursos pelo site de administração
# O "COURSEADMIN" chama a classe de personalização

class EnrollmentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'created_at']
    search_fields = ['user', 'course']

# Relaciona diretamente a tabela Material a tabela Aulas, o que permite uma criação mais fácil de objetos
class MaterialInlineAdmin(admin.TabularInline):
    model = Material

class LessonAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'course', 'release_date', 'created_at']
    search_fields = ['name', 'course']
    list_filter = ['created_at']

    inlines = [
        MaterialInlineAdmin
    ]

admin.site.register(Enrollments, EnrollmentsAdmin)
admin.site.register([Announcements, Comments])
admin.site.register(Lesson, LessonAdmin)
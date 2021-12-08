from django.contrib import admin

from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'start_date'] #Informações exibidas nas listas de cursos
    search_fields = ['name', 'slug'] #Define os espaços onde pesquisar 

    prepopulated_fields = {'slug' : ('name',)} #Recomenda automaticamente um atalho com base no nome do curso
                                               #OBS : A vírgula é estritamente necessária, caso contrário não será reconhecido uma lista

admin.site.register(Course, CourseAdmin) #Possibilita a alteração dos cursos pelo site de administração
# O "COURSEADMIN" chama a classe de personalização
from django.contrib import admin

from Simplemooc.forum.models import Reply, Thread

# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    search_fields = ['title', 'user__email']
    prepopulated_fields = {'slug' : ('title',)}

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'thread', 'created_at', 'updated_at']
    search_fields = ['thread', 'author__email']

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
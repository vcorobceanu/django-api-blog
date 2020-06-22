from django.contrib import admin
from TaskManager.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned')
    ordering = ['title']


admin.site.register(Task, TaskAdmin)

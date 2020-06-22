from django.contrib import admin
from TaskManager.models import Task, MyUser


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned')
    ordering = ['title']


admin.site.register(Task, TaskAdmin)
admin.site.register(MyUser)

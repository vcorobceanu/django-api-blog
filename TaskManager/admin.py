from django.contrib import admin
from TaskManager.models import Task, Comment, Notification, TimeLog, Like, Exports

from TaskManager.models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned', 'status')
    ordering = ['title']


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(TimeLog)
admin.site.register(Like)
admin.site.register(Exports)
admin.site.register(Project)
admin.site.register(ProjectTask)

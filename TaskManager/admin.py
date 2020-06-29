from django.contrib import admin
from TaskManager.models import Task, Comment, Notification, TimeLog, Like, Exports


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned', 'status')
    ordering = ['title']


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(TimeLog)
admin.site.register(Like)
admin.site.register(Exports)

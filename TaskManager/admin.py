from django.contrib import admin
from TaskManager.models import Task, Comments, Notification


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned', 'status')
    ordering = ['title']


admin.site.register(Task, TaskAdmin)
admin.site.register(Comments)
admin.site.register(Notification)

from django.conf.urls import url
from django.conf.urls.static import static

from config import settings
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.list_view, name='list'),
    path('projects/', views.project_view, name='projects'),
    path('projects/<str:id>/', views.projectitem, name='projectitem'),
    path('task/<str:title>/', views.taskitem, name='taskitem'),
    path('newtask/', views.newtask, name='newtask'),
    path('newprojecttask/', views.newprojecttask, name='newprojecttask'),
    path('newproject/', views.newproject, name='newproject'),
    path('mytasks/', views.mytasks, name='mytasks'),
    path('completed_tasks/', views.closed_tasks, name='completed'),
    path('mynotifi/', views.notifications_view, name='mynotify'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('export/<str:type>/', views.export_view, name='export'),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

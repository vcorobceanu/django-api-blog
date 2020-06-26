from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import TaskDocumentView

# router = DefaultRouter()
# tasks = router.register(r'tasks',
#                         TaskDocumentView,
#                         basename='taskdocument')
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.list_view, name='list'),
    path('task/<str:title>/', views.taskitem, name='taskitem'),
    path('newtask/', views.newtask, name='newtask'),
    path('mytasks/', views.mytasks, name='mytasks'),
    path('completed_tasks/', views.closed_tasks, name='completed'),
    path('mynotifi/', views.notifications_view, name='mynotify'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('statistics/', views.statistics_view, name='statistics'),
    # url(r'^', include(router.urls)),
]

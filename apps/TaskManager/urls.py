from django.urls import path
from apps.TaskManager import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('list/', views.list_view),
    path('task/<str:title>/', views.taskitem),
    path('newtask/', views.newtask, name="newtask"),
    path('mytasks/', views.mytasks),
    path('completed_tasks/', views.closed_tasks),
    path('mynotifi/', views.notifications_view),
    path('notifications/', views.notifications_view)
]

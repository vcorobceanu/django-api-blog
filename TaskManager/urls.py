from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('register/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('list/', views.list_view),
    path('list/<str:title>/', views.taskitem),
    path('newtask/', views.newtask, name = "newtask"),
    path('mytasks/', views.mytasks),
]



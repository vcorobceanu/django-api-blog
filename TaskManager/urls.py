from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('list', views.list ,name = "list"),
    # path('/login', views.login),
    # path('/logout', views.logout),
]
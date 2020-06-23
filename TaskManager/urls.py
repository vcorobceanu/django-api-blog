from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('list/', views.list),
    path('newtask/', views.newtask, name="newtask"),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    # path('mytasks/', views.mytasks),
]


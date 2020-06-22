from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('list/', views.list),
    path('newtask/', views.newtask, name = "newtask"),
    # path('login/', django.contrib.auth.urls),
    path('logout/', views.logout),
    # path('mytasks/', views.mytasks),
]
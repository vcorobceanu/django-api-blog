from django.urls import path
from apps.task.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('task/', TaskListView.as_view()),
    path('task/<int:pk>/', TaskItemView.as_view()),
    path('task/post', TaskViewSet.as_view()),
    path('task/comments', CommentViewSet.as_view()),

]

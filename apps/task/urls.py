from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.task.views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('task/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskItemView.as_view(), name='task_by_id'),
    path('task/post', TaskViewSet.as_view(), name='post_task'),
    path('task/comments', CommentViewSet.as_view(), name='post_comm'),
    path('task/notifications', NotificationsView.as_view(), name='post_comm'),

]

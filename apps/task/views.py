from drf_util.decorators import serialize_decorator
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from apps.task.serializers import *


class TaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request):
        tasks = Task.objects.all()

        return Response(TaskSerializer(tasks, many=True).data)


class TaskItemView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request, pk):
        taskk = get_object_or_404(Task.objects.filter(pk=pk))
        comments = Comment.objects.filter(task=taskk)

        rez = ["Task : ", TaskSerializer(taskk).data, "Comments : ", CommentSerializer(comments, many=True).data]

        return Response(rez)


class TaskViewSet(GenericAPIView):
    serializer_class = TaskSerializer

    @serialize_decorator(TaskSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        task1 = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            author=validated_data['author'],
            assigned=validated_data['assigned'],
            status=validated_data['status'],
        )
        task1.save()

        return Response(TaskSerializer(task1).data)


class CommentViewSet(GenericAPIView):
    serializer_class = CommentSerializer

    @serialize_decorator(CommentSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        comment = Comment.objects.create(
            text=validated_data['text'],
            author=validated_data['author'],
            task=validated_data['task'],
        )
        comment.save()

        return Response(CommentSerializer(comment).data)


class RegisterUserView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    @serialize_decorator(RegisterSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            is_superuser=True,
            is_staff=True
        )
        user.set_password(validated_data['password'])
        user.save()

        return Response(RegisterSerializer(user).data)

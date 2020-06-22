from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

<<<<<<< HEAD
<<<<<<< HEAD
from django.contrib import messages
from django.http import HttpResponse
from .models import MyUser
from .forms import RegisterForm

def index(request):
    return render(request, 'TaskMan/index.html')

def register(request):
    alert = False
    if(request.method == 'POST'):
        try:
            form = RegisterForm(request.POST)
            form.save()
        except:
            alert = True

    context = {'form': form, 'alert': alert}

    return render(request, 'TascMan/register.html', context)
=======
from apps.TaskManager.models import Task
from apps.TaskManager.serializers import TaskSerializer
=======
from TaskManager.models import Task
from TaskManager.serializers import TaskSerializer

>>>>>>> c6909e722692c025bebb514b010323190bb934d8

class TaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        tasks = Task.objects.all()

        return Response(TaskSerializer(tasks, many=True).data)
>>>>>>> b5f371ca2ba96ebafa892f3992c16578c19521aa

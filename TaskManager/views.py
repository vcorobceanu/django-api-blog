from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task
from .serializers import TaskSerializer

from django.shortcuts import render, redirect
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
    form = RegisterForm()
    context = {'form': form, 'alert': alert}

    return render(request, 'TaskMan/register.html', context)


class TaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        tasks = Task.objects.all()

        return Response(TaskSerializer(tasks, many=True).data)

def list(request):

    tsk = Task.objects.all()

    context = {
        't': tsk
    }

    return render(request, 'list.html', context)
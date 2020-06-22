from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task
from .serializers import TaskSerializer

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm


def index(request):
    return render(request, 'TaskMan/index.html')


def register(request):
    alert = False
    if (request.method == 'POST'):
        try:
            form = RegisterForm(request.POST)
            user = User.objects.create(
                first_name=form.data['first_name'],
                last_name=form.data['last_name'],
                username=form.data['username'],
                is_superuser=False,
                is_staff=True
            )
            user.set_password(form.data['password'])
            user.save()

            return redirect('/TaskManager/login')
        except:
            alert = True
    form = RegisterForm()
    context = {'form': form, 'alert': alert}

    return render(request, 'TaskMan/register.html', context)


def login(request):
    alert = False
    if (request.method == 'POST'):
        form = LoginForm(request.POST)

    form = LoginForm()
    context = {'form': form, 'alert': alert}

    return render(request, 'TaskMan/login.html', context)


def logout(request):
    try:
        del request.session['userlogin']
    except:
        pass

    return redirect('/')


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

    return render(request, 'TaskMan/list.html', context)


def newtask(request):
    people = MyUser.objects.all()

    context = {
        'p': people
    }

    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('description') and request.POST.get('people') and \
                request.session['userlogin']:
            task = Task()
            people = MyUser()
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.author = MyUser.objects.get(login=request.session['userlogin'])
            task.assigned = MyUser.objects.get(login=request.POST.get('people'))
            print(MyUser.objects.get(login=request.session['userlogin']))
            people.login = request.POST.get('people')
            task.save()

        return render(request, 'TaskMan/newtask.html', context)

    else:
        return render(request, 'TaskMan/newtask.html', context)

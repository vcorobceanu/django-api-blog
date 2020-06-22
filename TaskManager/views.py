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
from .forms import RegisterForm, LoginForm

def index(request):

    return render(request, 'TaskMan/index.html')

def register(request):
    alert = False
    if(request.method == 'POST'):
        try:
            form = RegisterForm(request.POST)
            form.save()
            return redirect('/login')
        except:
            alert = True
    form = RegisterForm()
    context = {'form': form, 'alert': alert}

    return render(request, 'TaskMan/register.html', context)


def login(request):
    alert = False
    if(request.method == 'POST'):
            form = LoginForm(request.POST)

            ok = False
            for user in MyUser.objects.all():
                if user.login==form.data['login'] and user.passw==form.data['passw']:
                    ok = True
                    rez_user = user

            if ok == True:
                request.session['userpass'] = rez_user.passw
                return redirect("/TaskManager")
            else:
                alert = True

    form = LoginForm()
    context = {'form': form, 'alert': alert}

    return render(request, 'TaskMan/login.html', context)

def logout(request):
    try:
        del request.session['userpass']
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
            'p' : people
    }

    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('description') and request.POST.get('people'):
                task = Task()
                people = MyUser()
                task.title = request.POST.get('title')
                task.description = request.POST.get('description')
                people.login = request.POST.get('people')
                task.save()

        return render(request, 'TaskMan/newtask.html', context)

    else:
        return render(request, 'TaskMan/newtask.html', context)
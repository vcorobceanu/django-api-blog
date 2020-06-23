from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Task

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm


def index(request):
    context = {'user': request.user}
    return render(request, 'TaskMan/index.html', context)


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


def login_view(request):
    alert = False
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        user = authenticate(request, username=form.data['username'], password=form.data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/TaskManager/list')
            else:
                alert = True
        else:
            alert = True

    form = LoginForm()
    context = {'form': form, 'alert': alert}

    return render(request, 'TaskMan/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/TaskManager')


def list(request):
    tsk = Task.objects.all()

    context = {
        't': tsk
    }

    return render(request, 'TaskMan/list.html', context)


def newtask(request):
    people = User.objects.all()
    context = {
        'p': people
    }
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('description') and request.POST.get('people') and request.user.is_authenticated:
            task = Task()
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.author = request.user
            task.assigned = User.objects.get(username=request.POST.get('people'))
            task.save()

        return redirect('/TaskManager/list')
    else:
        return render(request, 'TaskMan/newtask.html', context)

def taskitem(request, title):
    print(title)
    task = Task.objects.get(title=title)
    context = {'task': task}
    return render(request,'TaskMan/task_info.html', context)
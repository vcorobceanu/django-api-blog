from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Task, Comment
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from .alter_fuctions import add_not


def index(request):
    context = {'user': request.user}
    return render(request, 'TaskMan/index.html', context)


def register(request):
    alert = False
    if request.method == 'POST':
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
    if request.method == 'POST':
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


def list_view(request):
    task = Task.objects.all()

    context = {
        'task': task
    }

    return render(request, 'TaskMan/list.html', context)


def newtask(request):
    people = User.objects.all()
    context = {
        'people': people,
        'loget_user': request.user
    }
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('title') and request.POST.get('description') and request.POST.get(
                'people') and request.user.is_authenticated:
            task = Task()
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.author = request.user
            if 'post' in request.POST:
                task.assigned = User.objects.get(username=request.POST.get('people'))
            else:
                task.assigned = request.user
            task.save()
            add_not(task.assigned, 'Task is assigned to you')
            return redirect('/TaskManager/list')

    return render(request, 'TaskMan/newtask.html', context)


def taskitem(request, title):
    task = Task.objects.get(title=title)
    context = {'task': task}
    return render(request, 'TaskMan/task_info.html', context)


def mytasks(request):
    tasks = Task.objects.filter(assigned=request.user)
    context = {'task': tasks}
    return render(request, 'TaskMan/list.html', context)


def closed_tasks(request):
    tasks = Task.objects.filter(status='closed')
    context = {'task': tasks}
    return render(request, 'TaskMan/list.html', context)

def complete_task(request):
    task = Task.object.get(title=request.title)
    task.status = "closed"
    task.save
    context = {'task': task}
    return redirect(request, 'TaskMan/list.html', context)


def delete_task(request):
    task = Task.objects.get(title=request.title)
    task.delete()
    context = {'task': task}
    return redirect(request, 'TaskMan/list.html', context)


def coment(request):
    coment = Comment.objects.all()
    context = {
        'loget_user': request.user,
        'c': coment
    }
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('text') and request.user.is_authenticated:
            comment = Comment()
            comment.text = request.POST.get('title')
            comment.author = request.user

            comment.save()
            return redirect('/TaskManager/task_info')

    return render(request, 'TaskMan/task_info.html', context)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Task, Comment, Notification, TimeLog
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .notes_fuctions import add_not, notes_count


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


@login_required()
def list_view(request):
    task = Task.objects.all().order_by('-status')
    context = {
        'task': task,
        'count_notes': notes_count(request)
    }
    return render(request, 'TaskMan/list.html', context)


@login_required()
def newtask(request):
    people = User.objects.all()
    context = {
        'people': people,
        'loget_user': request.user
    }
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('title') and request.POST.get('description') and request.user.is_authenticated:
            try:
                task = Task()
                task.title = request.POST.get('title')
                task.description = request.POST.get('description')
                task.author = request.user
                if 'post' in request.POST:
                    task.assigned = User.objects.get(username=request.POST.get('people'))
                else:
                    task.assigned = request.user
                if request.POST.get('date') and request.POST.get('time'):
                    task.time_end = request.POST.get('date') + ' ' + request.POST.get('time')
                    task.timer_status = True
                task.save()
                add_not(task.assigned, 'Task is assigned to you by ' + task.author.username, task)
                return redirect('/TaskManager/list')
            except:
                return redirect('/TaskManager/list')

    return render(request, 'TaskMan/newtask.html', context)


@login_required()
def taskitem(request, title):
    task = Task.objects.get(title=title)
    coment = Comment.objects.filter(task=task)
    time_logs = task.timelog_set.all()
    context = {'task': task,
               'loget_user': request.user,
               'c': coment,
               'time_logs': time_logs, }

    if request.method == 'POST':
        if request.POST.get('description') and request.user.is_authenticated:
            comment = Comment()
            comment.text = request.POST.get('description')
            comment.author = request.user
            comment.task = task
            comment.save()
            add_not(task.author, 'Your task is been commented by ' + comment.author.username, task)
        if 'Complete' in request.POST:
            task.status = "closed"
            task.save()
            authors = set(task.comment_set.all().values_list('author_id', flat=True))
            notification_text = 'Task ' + task.title + ' is complited'
            for id in authors:
                add_not(User.objects.get(pk=id), notification_text, task)
            return render(request, 'TaskMan/task_info.html', context)
        if 'Delete' in request.POST:
            task.delete()
            return redirect('/TaskManager/list')
        if 'start_stop' in request.POST:
            if task.is_started == True:
                task.is_started = False
                timelog = TimeLog.objects.filter(task=task).latest('id')
                timelog.time_end = datetime.now()
                timedelta = timelog.time_end - timelog.time_begin
                timelog.total_time = datetime(timedelta)
                print(timelog.total_time)
                timelog.save()
            else:
                task.is_started = True
                timelog = TimeLog.objects.create(
                    task=task,
                    time_begin=datetime.now()
                )
                timelog.save()
            task.save()
        if 'find_date' in request.POST:
            context['time_logs'] = task.timelog_set.filter(time_begin__date=request.POST.get('date_input'))

    return render(request, 'TaskMan/task_info.html', context)


@login_required()
def mytasks(request):
    tasks = Task.objects.filter(assigned=request.user).order_by('-status')
    context = {
        'task': tasks,
        'count_notes': notes_count(request)
    }
    return render(request, 'TaskMan/list.html', context)


@login_required()
def closed_tasks(request):
    tasks = Task.objects.filter(status='closed')
    context = {
        'task': tasks,
        'count_notes': notes_count(request)
    }
    return render(request, 'TaskMan/list.html', context)


@login_required()
def coment(request):
    coment = Comment.objects.get()
    context = {
        'loget_user': request.user,
        'c': coment
    }
    if request.method == 'POST':
        if request.POST.get('description') and request.user.is_authenticated:
            comment = Comment()
            comment.text = request.POST.get('description')
            comment.author = request.user

            comment.save()
            return redirect('/TaskManager/task_info')

    return render(request, 'TaskMan/task_info.html', context)


@login_required()
def notifications_view(request):
    notes = Notification.objects.filter(assigned=request.user).order_by('-pk')
    context = {'notes': list(notes)}
    notes.update(seen=True)
    return render(request, 'TaskMan/mynotifi.html', context)

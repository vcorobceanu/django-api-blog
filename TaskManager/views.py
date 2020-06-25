from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Sum

from .models import Task, Comment, Notification, TimeLog, Like
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .notes_fuctions import add_not, notes_count

import time


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
    time_logs = task.timelog_set.filter(user=request.user)
    total_duration = time_logs.aggregate(Sum('duration'))
    is_liked = task.like_set.filter(user=request.user).exists()
    context = {'task': task,
               'loget_user': request.user,
               'c': coment,
               'time_logs': time_logs,
               'total_duration': total_duration,
               'is_liked': is_liked}

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
            notification_text = 'Task ' + task.title + ' is completed'
            for id in authors:
                add_not(User.objects.get(pk=id), notification_text, task)
            return render(request, 'TaskMan/task_info.html', context)
        if 'Delete' in request.POST:
            task.delete()
            return redirect('/TaskManager/list')
        if 'start_stop' in request.POST:
            if task.is_started:
                task.is_started = False
                timelog = TimeLog.objects.filter(task=task).filter(user=request.user).latest('id')
                timelog.time_end = datetime.now()
                last = timelog.duration
                print(last)
                timelog.duration = last + timelog.time_end - timelog.time_begin
                timelog.save()
                context['total_duration'] = task.timelog_set.filter(user=request.user).aggregate(Sum('duration'))
            else:
                task.is_started = True
                try:
                    last_log = TimeLog.objects.filter(task=task).filter(user=request.user).latest('id').duration
                except:
                    last_log = datetime.now() - datetime.now()
                timelog = TimeLog.objects.create(
                    task=task,
                    user=request.user,
                    time_begin=datetime.now(),
                    duration=last_log
                )
                timelog.save()
            task.save()
        if 'find_date' in request.POST:
            times = task.timelog_set.filter(user=request.user).filter(time_begin__date=request.POST.get('date_input'))
            context['time_logs'] = times
            context['total_duration'] = times.aggregate(Sum('duration'))
        if 'like' in request.POST:
            if task.like_set.filter(user=request.user).exists():
                like = task.like_set.get(user=request.user)
                like.delete()
                context['is_liked'] = False
            else:
                like = Like.objects.create(task=task, user=request.user)
                like.save()
                context['is_liked'] = True

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


@login_required()
def statistics_view(request):
    user = request.user

    last_month = datetime.today() - timedelta(days=30)
    time_logs = set(user.timelog_set.order_by('time_begin__date').values_list('time_begin__date', flat=True))
    stat = {}
    stats = []
    for date in time_logs:
        if date >= last_month.date():
            stat['date'] = date
            stat['duration'] = TimeLog.objects.filter(time_begin__date=date).latest('id').duration
            stats.append(stat.copy())

    tasks_id = set(user.timelog_set.values_list('task_id', flat=True))
    task_d = {}
    tasks = []
    for task_id in tasks_id:
        task = Task.objects.get(id=task_id)
        time_log = task.timelog_set.latest('id').duration
        task_d['task_info'] = task
        task_d['duration'] = time_log
        tasks.append(task_d.copy())
    try:
        tasks.sort(reverse=True, key=sortFunc)
    except:
        pass
    context = {'title': 'Statistics',
               'stats': stats,
               'tasks': tasks[:20]}
    return render(request, 'TaskMan/statistics.html', context)


def sortFunc(e):
    return e['duration']

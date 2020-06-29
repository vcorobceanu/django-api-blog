from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from elasticsearch import Elasticsearch

from .exports import in_csv, from_excel
from .forms import RegisterForm, LoginForm
from .models import *
from .notes_fuctions import add_not, notes_count


def index(request):
    context = {'title': 'Main page', 'user': request.user}
    return render(request, 'TaskMan/index.html', context)


def register(request):
    alert = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
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
        else:
            alert = form.errors

    form = RegisterForm()
    context = {'title': 'Register', 'form': form, 'alert': alert}

    return render(request, 'TaskMan/register.html', context)


def login_view(request):
    alert = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(request, username=form.data['username'], password=form.data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/TaskManager/list')
            else:
                alert = 'User not exist'
        else:
            alert = 'User not exist'

    form = LoginForm()
    context = {'title': 'Log in', 'form': form, 'alert': alert}
    print(alert)
    return render(request, 'TaskMan/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/TaskManager')


def title_notes(request, title):
    count_notes = notes_count(request)
    if count_notes != 0:
        title = title + ' (' + str(count_notes) + ')'
    return title


@login_required()
def list_view(request):
    task = Task.objects.all().order_by('-status')
    context = {
        'title': title_notes(request, 'List'),
        'task': task,
        'count_notes': notes_count(request)
    }
    return render(request, 'TaskMan/list.html', context)


@login_required()
def project_view(request):
    project = Project.objects.all()
    context = {
        'project': project
    }
    return render(request, 'TaskMan/projects.html', context)


@login_required()
def newproject(request):
    people = User.objects.all()
    context = {
        'title': 'New project',
        'people': people,
        'loget_user': request.user
    }
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('description') and request.POST.get('myfile'):
            project = Project()
            project.name = request.POST.get('name')
            project.description = request.POST.get('name')
            project.photo = request.POST.get('myfile')
            project.author = request.user
            project.save()

    return render(request, 'TaskMan/newproject.html', context)


@login_required()
def newtask(request):
    people = User.objects.all()
    context = {
        'title': 'New task',
        'people': people,
        'loget_user': request.user
    }
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('description'):
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
                task.timer_status = False
            task.save()
            add_not.delay(task.assigned.id, 'Task is assigned to you by ' + task.author.username, task.id)
            return redirect('/TaskManager/list')

    return render(request, 'TaskMan/newtask.html', context)


def newprojecttask(request, id):
    people = User.objects.all()
    ptask = Project.objects.all()
    context = {
        'title': 'New project task',
        'people': people,
        'loget_user': request.user,
        'name': id,
    }
    if request.method == 'POST':
        if request.POST.get('title1') and request.POST.get('description1'):
            task = ProjectTask()
            task.title = request.POST.get('title1')
            task.description = request.POST.get('description1')
            task.author = request.user
            task.project = ptask.get('id')

    return render(request, 'TaskMan/newprojecttask.html', context)


@login_required()
def taskitem(request, title):
    task = Task.objects.get(title=title)
    coment = Comment.objects.filter(task=task)
    time_logs = task.timelog_set.filter(user=request.user)
    total_duration = None
    if time_logs.exists():
        total_duration = time_logs.latest('id')
    is_liked = task.like_set.filter(user=request.user).exists()
    context = {'title': title,
               'task': task,
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
            add_not.delay(task.author.id, 'Your task is been commented by ' + comment.author.username, task.id)
        if 'Complete' in request.POST:
            task.status = "closed"
            task.save()
            authors = set(task.comment_set.all().values_list('author_id', flat=True))
            notification_text = 'Task ' + task.title + ' is completed'
            for id in authors:
                add_not.delay(id, notification_text, task.id)
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
                timelog.duration = last + timelog.time_end - timelog.time_begin
                timelog.save()
                context['total_duration'] = None
                if task.timelog_set.filter(user=request.user).exists():
                    context['total_duration'] = task.timelog_set.filter(user=request.user).latest('id')
            else:
                task.is_started = True
                last_log = None
                if TimeLog.objects.filter(task=task).filter(user=request.user).exists():
                    last_log = TimeLog.objects.filter(task=task).filter(user=request.user).latest('id').duration
                if last_log is None:
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
            if request.POST.get('date_input'):
                times = task.timelog_set.filter(user=request.user).filter(
                    time_begin__date=request.POST.get('date_input'))
                if times.exists():
                    context['time_logs'] = times
                    context['total_duration'] = times.latest('id')
        if 'like' in request.POST:
            if task.like_set.filter(user=request.user).exists():
                like = task.like_set.get(user=request.user)
                like.delete()
                context['is_liked'] = False
            else:
                like = Like.objects.create(task=task, user=request.user)
                like.save()
                context['is_liked'] = True
                text = 'Your task was liked by ' + request.user.username
                add_not.delay(task.author.id, text, task.id)

    return render(request, 'TaskMan/task_info.html', context)


@login_required()
def projectitem(request, id):
    ptask = ProjectTask.objects.filter(project=id)
    pro = Project.objects.all()
    context = {
        'ptask': ptask,
        'pro': pro,
        'name': id,
    }
    return render(request, 'TaskMan/project_tasks.html', context)


@login_required()
def mytasks(request):
    tasks = Task.objects.filter(assigned=request.user).order_by('-status')
    context = {
        'title': title_notes(request, 'My tasks'),
        'task': tasks,
        'count_notes': notes_count(request)
    }
    return render(request, 'TaskMan/list.html', context)


@login_required()
def closed_tasks(request):
    tasks = Task.objects.filter(status='closed')
    context = {
        'title': title_notes(request, 'Closed tasks'),
        'task': tasks,
        'count_notes': notes_count(request)
    }
    return render(request, 'TaskMan/list.html', context)


@login_required()
def coment(request):
    coment = Comment.objects.get()
    context = {
        'title': 'Comment',
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
    context = {'title': 'Notifications', 'notes': list(notes)}
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
        tasks.sort(reverse=True, key=sortFunc)
    context = {'title': 'Statistics',
               'stats': stats,
               'tasks': tasks[:20]}
    return render(request, 'TaskMan/statistics.html', context)


def sortFunc(e):
    return e['duration']


def search(request):
    s_key = request.POST.get('abc')
    print(s_key)
    if s_key:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        query = es.search(index="search",
                          body={'query': {'fuzzy': {'title': s_key}}})['hits']
        sub = query['hits']
        tasks = []
        for record in sub:
            source = record.get('_source', {})
            tasks = tasks + source
    else:
        print('10')
        tasks = 'None'

    return render(request, 'TaskMan/search.html', {'tasks': tasks})


@login_required()
def export_view(request, type):
    if type == 'excel':
        return from_excel(request)
    else:
        return in_csv(request)

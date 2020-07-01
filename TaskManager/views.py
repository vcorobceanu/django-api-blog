import os
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users
from .elastic import search, indexing, delete_task_index
from .exports import in_csv, from_excel
from .forms import *
from .models import *
from .notes_fuctions import add_not, notes_count


def index(request):
    context = {'title': 'Main page', 'user': request.user}
    return render(request, 'TaskMan/index.html', context)


@unauthenticated_user
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
                is_staff=True,
            )
            user.set_password(form.data['password'])
            user.save()
            return redirect('/TaskManager/login')
        else:
            alert = form.errors

    form = RegisterForm()
    context = {'title': 'Register', 'form': form, 'alert': alert}

    return render(request, 'TaskMan/register.html', context)


@unauthenticated_user
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
    if request.GET:
        exp = Exports.objects.filter(user=request.user).last()

        if exp is not None:

            if exp.csv is not None:
                task_id = exp.csv
                exp.exp_info = 'Export all task info in CSV'
                exp.save()
                return redirect('export_file', 'csv', task_id)

            if exp.excel is not None:
                task_id = exp.excel
                exp.exp_info = 'Export all task info in XLS'
                exp.save()
                return redirect('export_file', 'excel', task_id)

    loget_user = request.user
    task = Task.objects.filter(Q(assigned=loget_user) | Q(author=loget_user)).order_by('-status')

    if loget_user.is_superuser:
        task = Task.objects.all().order_by('title').order_by('-status')

    parent = Subtasks.objects.all()

    serch = False
    s_key = request.POST.get('abc')
    lis = []

    if s_key:
        lis = search(request)

    if lis:
        task = lis
        serch = True

    context = {
        'title': title_notes(request, 'List'),
        'task': task,
        'parent': parent,
        'count_notes': notes_count(request),
        'export_menu': True,
        'serch': serch
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
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        nestle = Project.objects.create(
            name=form.data['name'],
            description=form.data['description'],
            photo=request.FILES.get('photo'),
            author=request.user
        )
        group = Group.objects.get(name='project_administrator')
        group.user_set.add(request.user)
        nestle.save()
    else:
        form = NewProjectForm()
    return render(request, 'TaskMan/newproject.html', {'form': form})


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

            task.save()

            indexing(task)

            add_not.delay(task.assigned.id, 'Task is assigned to you by ' + task.author.username, task.id)

            return redirect('/TaskManager/list')

    return render(request, 'TaskMan/newtask.html', context)


@login_required()
def newsubtask(request, title):
    people = User.objects.all()
    context = {
        'title': title,
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

            subtask = Subtasks()
            parent_task = Task.objects.get(title=title)
            subtask.parent_task = parent_task
            subtask.subtask = task
            task.depth = parent_task.depth + 1

            task.save()
            subtask.save()
            indexing(task)

            add_not.delay(task.assigned.id, 'Task is assigned to you by ' + task.author.username, task.id)

            return redirect('/TaskManager/list')

    return render(request, 'TaskMan/newsubtask.html', context)


@allowed_users(allowed_roles=['admin', 'project_administrator'])
def newprojecttask(request, id):
    if Project.objects.get(id=id).author == request.user or request.user.is_superuser:
        people = User.objects.all()
        ptask = Project.objects.all()
        context = {
            'title': Project.objects.get(id=id).name,
            'people': people,
            'loget_user': request.user
        }

        if request.method == 'POST':
            if request.POST.get('title1') and request.POST.get('description1'):
                task = ProjectTask()
                task.title = request.POST.get('title1')
                task.description = request.POST.get('description1')
                task.author_p = request.user
                task.project = ptask.get(pk=id)
                if 'post' in request.POST:
                    task.assigned = User.objects.get(username=request.POST.get('people'))
                else:
                    task.assigned = request.user
                task.save()

        return render(request, 'TaskMan/newprojecttask.html', context)

    else:
        return HttpResponse('You are not authorized')


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
            indexing(task)
            authors = set(task.comment_set.all().values_list('author_id', flat=True))
            notification_text = 'Task ' + task.title + ' is completed'
            for id in authors:
                add_not.delay(id, notification_text, task.id)
            return render(request, 'TaskMan/task_info.html', context)

        if 'Delete' in request.POST:
            delete_task_index(task)
            task.delete()
            return redirect('/TaskManager/list')

        if 'Subtask' in request.POST:
            return redirect(request, '/TaskMan/newsubtask', context)

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


def newprojectsubtask(request, title):
    people = User.objects.all()
    context = {
        'title': title,
        'people': people,
        'loget_user': request.user
    }

    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('description'):
            task = ProjectTask()
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.author_p = request.user

            if 'post' in request.POST:
                task.assigned = User.objects.get(username=request.POST.get('people'))
            else:
                task.assigned = request.user

            subtask = Subtasks()
            subtask.projectparent_task = ProjectTask.objects.get(title=title)
            subtask.projectsubtask = task
            depth = ProjectTask.objects.get(id=subtask.projectparent_task.id).depth

            if depth:
                task.depth = depth + 1
            else:
                task.depth = 0

            task.save()
            subtask.save()
            indexing(task)

            add_not.delay(task.assigned.id, 'Task is assigned to you by ' + task.author_p.username, task.id)

            return redirect('/TaskManager/projects')

    return render(request, 'TaskMan/newprojectsubtask.html', context)


@login_required()
def projecttaskitem(request, id, title):
    pro = Project.objects.all()
    pptask = ProjectTask.objects.get(id=title)
    coment = Comment.objects.filter(projecttask=pptask)
    time_logs = pptask.timelog_set.filter(user=request.user)
    total_duration = None
    is_liked = pptask.like_set.filter(user=request.user).exists()

    if time_logs.exists():
        total_duration = time_logs.latest('id')
    context = {
        'project': pro,
        'title': title,
        'projecttask': pptask,
        'pc': coment,
        'name': id,
        'az': pptask,
        'loget_user': request.user,
        'time_logs': time_logs,
        'total_duration': total_duration,
        'is_liked': is_liked
    }

    if request.method == 'POST':
        if request.POST.get('description') and request.user.is_authenticated:
            comment = Comment()
            comment.text = request.POST.get('description')
            comment.author = request.user
            comment.projecttask = pptask
            comment.save()
            add_not.delay(pptask.author_p.id,
                          'Your task is been commented by ' + comment.author.username + ' in ' + comment.projecttask.title,
                          pptask.id)

        if 'Complete' in request.POST:
            pptask.status = "closed"
            pptask.save()
            indexing(pptask)
            authors = set(pptask.comment_set.all().values_list('author_id', flat=True))
            notification_text = 'Task ' + pptask.title + ' is completed'
            for id in authors:
                add_not.delay(id, notification_text, pptask.id)
            return render(request, 'TaskMan/project_task_info.html', context)

        if 'Delete' in request.POST:
            delete_task_index(pptask)
            pptask.delete()
            return redirect('/TaskManager/projects')

        if 'Subtask' in request.POST:
            return redirect(request, '/TaskMan/newprojectsubtask', context)

        if 'start_stop' in request.POST:
            if pptask.is_started:
                pptask.is_started = False
                timelog = TimeLog.objects.filter(task=pptask).filter(user=request.user).latest('id')
                timelog.time_end = datetime.now()
                last = timelog.duration
                timelog.duration = last + timelog.time_end - timelog.time_begin
                timelog.save()
                context['total_duration'] = None
                if pptask.timelog_set.filter(user=request.user).exists():
                    context['total_duration'] = pptask.timelog_set.filter(user=request.user).latest('id')
            else:
                pptask.is_started = True
                last_log = None
                if TimeLog.objects.filter(projecttask=pptask).filter(user=request.user).exists():
                    last_log = TimeLog.objects.filter(projecttask=pptask).filter(user=request.user).latest(
                        'id').duration
                if last_log is None:
                    last_log = datetime.now() - datetime.now()

                timelog = TimeLog.objects.create(
                    projecttask=pptask,
                    user=request.user,
                    time_begin=datetime.now(),
                    duration=last_log
                )
                timelog.save()
            pptask.save()
        if 'find_date' in request.POST:
            if request.POST.get('date_input'):
                times = pptask.timelog_set.filter(user=request.user).filter(
                    time_begin__date=request.POST.get('date_input'))
                if times.exists():
                    context['time_logs'] = times
                    context['total_duration'] = times.latest('id')
        if 'like' in request.POST:
            if pptask.like_set.filter(user=request.user).exists():
                like = pptask.like_set.get(user=request.user)
                like.delete()
                context['is_liked'] = False
            else:
                like = Like.objects.create(projecttask=pptask, user=request.user)
                like.save()
                context['is_liked'] = True
                text = 'Your task was liked by ' + request.user.username
                add_not.delay(pptask.author_p.id, text, pptask.id)

    return render(request, 'TaskMan/project_task_info.html', context)


@login_required()
def projectitem(request, id):
    pro = Project.objects.get(pk=id)
    ptask = ProjectTask.objects.filter(project=id)

    context = {
        'ptask': ptask,
        'pro': pro,
        'name': id,
    }
    return render(request, 'TaskMan/project_tasks.html', context)


@login_required()
def mytasks(request):
    tasks = Task.objects.filter(author=request.user).order_by('-status')
    s_key = request.POST.get('abc')
    lis = []

    if s_key:
        lis = search(request)

    if lis:
        tasks = lis

    context = {
        'title': title_notes(request, 'My tasks'),
        'task': tasks,
        'count_notes': notes_count(request)
    }
    return render(request, 'TaskMan/list.html', context)


@login_required()
def closed_tasks(request):
    tasks = Task.objects.filter(status='closed')
    s_key = request.POST.get('abc')
    lis = []

    if s_key:
        lis = search(request)

    if lis:
        tasks = lis

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


def projectcoment(request):
    pcoment = Comment.objects.get()
    context = {
        'title': 'Comment',
        'loget_user': request.user,
        'pc': pcoment
    }
    if request.method == 'POST':
        if request.POST.get('description') and request.user.is_authenticated:
            comment = Comment()
            comment.text = request.POST.get('description')
            comment.author = request.user

            comment.save()
            return redirect('/TaskManager/project_task_info.html')

    return render(request, 'TaskMan/project_task_info.html', context)


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
        if task_id:
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


@login_required()
def export_view(request, type):
    # clear_exports.delay()

    exp = Exports.objects.create(user=request.user)

    if type == 'excel':
        task = from_excel.delay(request.user.id)
        exp.excel = task.id

    else:
        task = in_csv.delay(request.user.id)
        exp.csv = task.id

    exp.save()

    return redirect('list')


def export_file_view(request, filetype, filename):
    path = 'exports/' + filename

    response = None
    if filetype == 'excel':
        path = path + '.xls'

        if os.path.exists(path):
            with open(path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/ms-excel')
                response['Content-Disposition'] = 'inline; filename="TaskList.xls"'

    else:
        path = path + '.csv'
        if os.path.exists(path):
            with open(path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = 'inline; filename="TaskList.csv"'

    if response:
        return response
    else:
        return HttpResponse('<h1>File is deleted</h1>')


@login_required()
def export_list_view(requset):
    if requset.user.is_superuser:
        exports = Exports.objects.all().order_by('date')
    else:
        exports = Exports.objects.filter(user=requset.user).order_by('date')

    context = {'title': 'Exports list', 'exports': exports}

    return render(requset, 'TaskMan/exports_list.html', context)


@login_required()
@allowed_users(allowed_roles=['admin'])
def users_view(request):
    users = User.objects.all().exclude(username=request.user.username).order_by('username')
    context = {
        'title': 'Users list',
        'users': users
    }
    return render(request, 'TaskMan/users.html', context)


@allowed_users(allowed_roles=['admin'])
def make_admin_view(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = True
    user.save()
    group = Group.objects.get(name='admin')
    group.user_set.add(user)
    return redirect('users_list')


@allowed_users(allowed_roles=['admin'])
def take_admin_view(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = False
    user.groups.remove(Group.objects.get(name='admin'))
    user.save()

    return redirect('users_list')

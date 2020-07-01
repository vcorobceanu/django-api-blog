import csv
import xlwt
import time
import os

from celery import shared_task
from django.contrib.auth.models import User
from .models import Task
from datetime import datetime
from django.db.models import Q


@shared_task
def in_csv(user_id):
    user = User.objects.get(id=user_id)

    with open("%s%s.csv" % ("exports/", in_csv.request.id), "w+") as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Description', 'Status', 'Comments count', 'Timelogs count', 'Total loget time'])

        tasks = Task.objects.filter(Q(assigned=user) | Q(author=user))

        if user.is_superuser:
            tasks = Task.objects.all()

        for task in tasks:
            last_log = None

            if task.timelog_set.filter(user=user).exists():
                last_log = task.timelog_set.filter(user=user).latest('id').duration

            if last_log is None:
                dtn = datetime.now()
                last_log = dtn - dtn

            writer.writerow([task.title, task.description, task.status, task.comment_set.count(),
                             task.timelog_set.filter(user=user).count(), last_log])


@shared_task
def from_excel(user_id):
    user = User.objects.get(id=user_id)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Tasks')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Title', 'Description', 'Status', 'Comments count', 'Timelogs count', 'Total loget time']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Task.objects.all().values_list('title', 'description', 'status')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    row_num = 0
    col_num = 3

    for task in Task.objects.all():
        row_num += 1
        last_log = None

        if task.timelog_set.filter(user=user).exists():
            last_log = task.timelog_set.filter(user=user).latest('id').duration

        if last_log is None:
                dtn = datetime.now()
                last_log = dtn - dtn

        ws.write(row_num, col_num, task.comment_set.count())
        ws.write(row_num, col_num + 1, task.timelog_set.filter(user=user).count())
        ws.write(row_num, col_num + 2, str(last_log))

    wb.save("%s%s.xls" % ("exports/", from_excel.request.id))


@shared_task(time_limit=10)
def clear_exports():
    file_dir = 'exports/'

    for path in os.listdir(file_dir):
        full_path = os.path.join(file_dir, path)

        if os.path.isfile(full_path):
            os.remove(full_path)

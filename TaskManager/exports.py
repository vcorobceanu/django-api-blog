import csv
import xlwt
import time
import os

from celery import shared_task
from django.contrib.auth.models import User
from .models import Task, Exports
from django.http import HttpResponse
from datetime import datetime


@shared_task
def in_csv(user_id):
    user = User.objects.get(id=user_id)

    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="TaskList.csv"'
    with open("%s%s.csv" % ("exports/", in_csv.request.id), "w+") as f:
        writer = csv.writer(f)
        time.sleep(2)
        writer.writerow(['Title', 'Description', 'Status', 'Comments count', 'Timelogs count', 'Total loget time'])
        for task in Task.objects.all():
            last_log = None
            if task.timelog_set.filter(user=user).exists():
                last_log = task.timelog_set.filter(user=user).latest('id').duration
            if last_log is None:
                last_log = datetime.now() - datetime.now()
            writer.writerow([task.title, task.description, task.status, task.comment_set.count(),
                             task.timelog_set.filter(user=user).count(), last_log])

    print('este')
    # return str(response._container)
    return True


@shared_task
def from_excel(user_id):
    user = User.objects.get(id=user_id)
    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="TaskList.xls"'

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

    # for i in range(10):
    #     print(1)
    time.sleep(2)

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
            last_log = datetime.now() - datetime.now()
        ws.write(row_num, col_num, task.comment_set.count())
        ws.write(row_num, col_num + 1, task.timelog_set.filter(user=user).count())
        ws.write(row_num, col_num + 2, str(last_log))

    wb.save("%s%s.xls" % ("exports/", from_excel.request.id))
    print('este')
    return True


@shared_task
def clear_exports():
    file_dir = 'exports/'
    for path in os.listdir(file_dir):
        full_path = os.path.join(file_dir, path)
        if os.path.isfile(full_path):
            os.remove(full_path)

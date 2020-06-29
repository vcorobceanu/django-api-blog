import csv
import xlwt

from celery import shared_task
from django.contrib.auth.models import User
from .models import Task, TimeLog, Comment
from django.http import HttpResponse
from datetime import datetime


@shared_task
def in_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="TaskList.csv"'
    writer = csv.writer(response)

    writer.writerow(['Title', 'Description', 'Status', 'Comments count', 'Timelogs count', 'Total loget time'])
    for task in Task.objects.all():
        last_log = None
        if task.timelog_set.filter(user=request.user).exists():
            last_log = task.timelog_set.filter(user=request.user).latest('id').duration
        if last_log is None:
            last_log = datetime.now() - datetime.now()
        writer.writerow([task.title, task.description, task.status, task.comment_set.count(),
                         task.timelog_set.filter(user=request.user).count(), last_log])
    return response


@shared_task
def from_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="TaskList.xls"'

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
        if task.timelog_set.filter(user=request.user).exists():
            last_log = task.timelog_set.filter(user=request.user).latest('id').duration
        if last_log is None:
            last_log = datetime.now() - datetime.now()
        ws.write(row_num, col_num, task.comment_set.count())
        ws.write(row_num, col_num + 1, task.timelog_set.filter(user=request.user).count())
        ws.write(row_num, col_num + 2, str(last_log))

    wb.save(response)
    return response

from time import *
from datetime import datetime
from .models import Task
from .notes_fuctions import add_not
from django.utils.timesince import timeuntil

import threading

def check_updates():
	while True:
		tasks = Task.objects.filter(timer_start=True)
		for task in tasks:
			if time_remaining(task.time_end)<=0:
				task.timer_start = False
				task.timer_status = False
				task.status = 'closed'
				task.save()
				print('1')
				add_not(task.author, 'Task is end', task)
		sleep(3)

def time_remaining(date):
	dif = (date - datetime.now()).total_seconds()
	return dif


def time_remaining_forview(date1, date2):
	print(date1.__class__.__name__)
	dif = (date1 - date2).total_seconds()
	dif = int(dif)
	if dif < 60:
		return str(int(dif))+" seconds"
	dif/=60
	if dif<60:
		return str(int(dif))+" minutes"
	dif/=60
	if dif<24:
		return str(int(dif))+" hours"
	dif/=24
	if dif<7:
		return str(int(dif))+" day"
	dif/=7
	if dif<4:
		return str(int(dif))+" week"

	return (date1.year - date2.year)*12 + (date1.month - date2.month)

check_updates_thread = threading.Thread(target=check_updates)
check_updates_thread.start()

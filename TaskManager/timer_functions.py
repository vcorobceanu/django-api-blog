from time import *
from .models import Task
from .notes_fuctions import add_not
from django.utils.timesince import timeuntil
from django.shortcuts import redirect

import threading


def countdown(time):
	mytimer = time
	for x in range(time):
		mytimer=mytimer-1
		sleep(1)

	print('Timer out')

def start_timer(time):
	countdown_thread = threading.Thread(target = countdown(time))
	countdown_thread.start()

def check_updates():
	while True:
		tasks = Task.objects.filter(timer_status=True)
		for task in tasks:
			if timeuntil(task.time_end)[0]=='0':
				task.timer_status = False
				task.status = 'closed'
				task.save()
				add_not(task.author, 'Task is end', task)
		sleep(60)

check_updates_thread = threading.Thread(target = check_updates)
check_updates_thread.start()

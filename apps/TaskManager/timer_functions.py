from time import *
import threading


def countdown():
    mytimer = 3
    for x in range(mytimer):
        mytimer = mytimer - 1
        sleep(1)

    print('Timer out')


def start_timer():
    countdown_thread = threading.Thread(target=countdown)
    countdown_thread.start()

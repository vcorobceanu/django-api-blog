from django.shortcuts import render

from django.contrib import messages
from django.http import HttpResponse
from .models import MyUser
from .forms import RegisterForm

def index(request):
    return render(request, 'TaskMan/index.html')

def register(request):
    alert = False
    if(request.method == 'POST'):
        try:
            form = RegisterForm(request.POST)
            form.save()
        except:
            alert = True

    context = {'form': form, 'alert': alert}

    return render(request, 'TascMan/register.html', context)
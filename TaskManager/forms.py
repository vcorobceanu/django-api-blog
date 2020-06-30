from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User
from django import forms
from .models import *


class RegisterForm(ModelForm):
    class Meta:
        model = User
        # fields = ['name', 'pren', 'login', 'passw']
        fields = ['first_name', 'last_name', 'username', 'password']

        widgets = {'first_name': TextInput(attrs={
            'style': 'margin-top: 10px;',
            'placeholder': 'First name',
            'required': True
            }),
            'last_name': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Last name',
                'required': True
            }),
            'username': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Username'
            }),
            'password': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Password',
                'type': 'password'
            }),
        }

        class NewTaskForm(ModelForm):
            class Meta:
                model = User
                fields = '__all__'


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Log in'
            }),
            'password': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Parola',
                'type': 'password'
            }),
        }


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'photo']

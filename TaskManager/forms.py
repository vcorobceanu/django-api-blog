from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User


class RegisterForm(ModelForm):
    class Meta:
        model = User
        # fields = ['name', 'pren', 'login', 'passw']
        fields = '__all__'

        widgets = {'first_name': TextInput(attrs={
            'style': 'margin-top: 10px;',
            'placeholder': 'Nume'
        }),
            'last_name': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Prenume'
            }),
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

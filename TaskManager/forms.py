from .models import MyUser
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
                model = MyUser
                fields = '__all__'

class LoginForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['login', 'passw']
        widgets = {
        'login': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Log in'
            }),
        'passw': TextInput(attrs={
                'style': 'margin-top: 10px;',
                'placeholder': 'Parola',
                'type': 'password'
            }),
        }
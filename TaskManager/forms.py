from .models import MyUser
from django.forms import ModelForm, TextInput

class RegisterForm(ModelForm):
    class Meta:
        model = MyUser
        # fields = ['name', 'pren', 'login', 'passw']
        fields = '__all__'

        widgets = {'name': TextInput(attrs={
            'style': 'margin-top: 10px;',
            'placeholder': 'Nume'
        }),
        'pren': TextInput(attrs={
            'style': 'margin-top: 10px;',
            'placeholder': 'Prenume'
        }),
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
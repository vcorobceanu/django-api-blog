from .models import MyUser
from django.forms import ModelForm, TextInput

class RegisterForm(ModelForm):
    class Meta:
        model = MyUser
        fields = '__all__'
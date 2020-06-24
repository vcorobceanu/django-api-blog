from django.test import TestCase
from TaskManager.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User


class RegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Billy', password='Milligan', first_name='1', last_name='2')

    def test_username_field_label(self):
        form = RegisterForm()
        self.assertEquals(form.fields['username'].label, 'Username')

    def test_password_field_label(self):
        form = RegisterForm()
        self.assertEquals(form.fields['password'].label, 'Password')

    def test_first_name_field_label(self):
        form = RegisterForm()
        self.assertEquals(form.fields['first_name'].label, 'First name')

    def test_last_name_field_label(self):
        form = RegisterForm()
        self.assertEquals(form.fields['last_name'].label, 'Last name')


class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Billy', password='Milligan')

    def test_username_field_label(self):
        form = LoginForm()
        self.assertEquals(form.fields['username'].label, 'Username')

    def test_password_field_label(self):
        form = LoginForm()
        self.assertEquals(form.fields['password'].label, 'Password')

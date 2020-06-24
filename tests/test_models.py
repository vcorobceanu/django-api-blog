from django.test import TestCase
from TaskManager.models import Task, Comment, Notification
from django.contrib.auth.models import User


class TaskModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='Billy', password='Milligan')
        Task.objects.create(title='Big', description='Bob', assigned=user, author=user)

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_description_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_author_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_assigned_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('assigned').verbose_name
        self.assertEquals(field_label, 'assigned')

    def test_status_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('assigned').verbose_name
        self.assertEquals(field_label, 'assigned')

    def test_timer_status_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('timer_status').verbose_name
        self.assertEquals(field_label, 'timer status')

    def test_timer_end_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('time_end').verbose_name
        self.assertEquals(field_label, 'time end')

    def test_title_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_status_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('status').max_length
        self.assertEquals(max_length, 32)

    def test_task_str_return(self):
        task = Task.objects.get(id=1)
        expected = task.title
        self.assertEquals(expected, str(task))

    def test_status_default(self):
        task = Task.objects.get(id=1)
        expected = task.status
        self.assertEquals(expected, 'open')

    def test_timer_status_default(self):
        task = Task.objects.get(id=1)
        expected = task.timer_status
        self.assertEquals(expected, False)


class CommentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='Billy', password='Milligan')
        Task.objects.create(title='Big', description='Bob', assigned=user, author=user)
        Comment.objects.create(text='text', author=user, task_id=1)

    def test_text_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_text_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('text').max_length
        self.assertEquals(max_length, 100)

    def test_task_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('task').verbose_name
        self.assertEquals(field_label, 'task')

    def test_author_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_comment_str_return(self):
        comment = Comment.objects.get(id=1)
        expected = comment.text
        self.assertEquals(expected, str(comment))


class NotificationModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='Billy', password='Milligan')
        Task.objects.create(title='Big', description='Bob', assigned=user, author=user)
        Notification.objects.create(assigned_id=1, info='Notification info', task_id=1)

    def test_notify_assigned_label(self):
        notification = Notification.objects.get(id=1)
        field_label = notification._meta.get_field('assigned').verbose_name
        self.assertEquals(field_label, 'assigned')

    def test_notify_info_label(self):
        notification = Notification.objects.get(id=1)
        field_label = notification._meta.get_field('info').verbose_name
        self.assertEquals(field_label, 'info')

    def test_notify_task_label(self):
        notification = Notification.objects.get(id=1)
        field_label = notification._meta.get_field('task').verbose_name
        self.assertEquals(field_label, 'task')

    def test_notify_seen_label(self):
        notification = Notification.objects.get(id=1)
        field_label = notification._meta.get_field('seen').verbose_name
        self.assertEquals(field_label, 'seen')

    def test_notify_info_max_length(self):
        notification = Notification.objects.get(id=1)
        max_length = notification._meta.get_field('info').max_length
        self.assertEquals(max_length, 399)

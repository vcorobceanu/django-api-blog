from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    STATUS = {
        ('open', 'Opened'),
        ('closed', 'Closed'),
    }

    title = models.CharField(max_length=100, db_index=True, unique=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    status = models.CharField(max_length=32, choices=STATUS, default='open', )
    is_started = models.BooleanField(default=0)

    def __str__(self):
        return self.title

    @property
    def status_indexing(self):
        return {'status': self.status}

    @property
    def is_started_indexing(self):
        return {'is_started': self.is_started}

    @property
    def assigned_indexing(self):
        return [assigned.username for assigned in self.assigned.all()]


class Comment(models.Model):
    text = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Notification(models.Model):
    assigned = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=399)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)


class Like(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Exports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    excel = models.CharField(max_length=100, blank=True, null=True)
    csv = models.CharField(max_length=100, blank=True, null=True)


class Project(models.Model):
    STATUS = {
        ('in_process', 'In process'),
        ('finished', 'Finished'),
    }

    name = models.CharField(max_length=100)
    description = models.TextField(unique=True)
    photo = models.ImageField(default='no_image.png', upload_to='project_image')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_project')
    status = models.CharField(max_length=32, choices=STATUS, default='in_process', )

    def __str__(self):
        return self.name


class ProjectTask(models.Model):
    STATUS = {
        ('open', 'Opened'),
        ('closed', 'Closed'),
    }

    title = models.CharField(max_length=100, db_index=True, unique=True)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    author_p = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_author')
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_project')
    status = models.CharField(max_length=32, choices=STATUS, default='open', )
    is_started = models.BooleanField(default=0)

    def __str__(self):
        return self.title

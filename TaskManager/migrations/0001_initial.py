# Generated by Django 3.0.7 on 2020-06-29 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(unique=True)),
                ('photo', models.ImageField(default='no_image.png', upload_to='project_image')),
                ('status', models.CharField(choices=[('in_process', 'In process'), ('finished', 'Finished')], default='in_process', max_length=32)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_project', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('closed', 'Closed'), ('open', 'Opened')], default='open', max_length=32)),
                ('is_started', models.BooleanField(default=0)),
                ('assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_begin', models.DateTimeField()),
                ('time_end', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TaskManager.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('closed', 'Closed'), ('open', 'Opened')], default='open', max_length=32)),
                ('is_started', models.BooleanField(default=0)),
                ('assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_project', to=settings.AUTH_USER_MODEL)),
                ('author_p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_author', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='TaskManager.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=399)),
                ('seen', models.BooleanField(default=False)),
                ('assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TaskManager.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TaskManager.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.CharField(blank=True, max_length=100, null=True)),
                ('csv', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TaskManager.Task')),
            ],
        ),
    ]

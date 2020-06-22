# Generated by Django 3.0.7 on 2020-06-22 05:40

import TaskManager.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0008_auto_20200622_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned',
            field=models.ForeignKey(default=TaskManager.models.MyUser, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='TaskManager.MyUser'),
        ),
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(default=TaskManager.models.MyUser, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='TaskManager.MyUser'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('closed', 'Closed'), ('open', 'Opened')], default='open', max_length=32),
        ),
    ]

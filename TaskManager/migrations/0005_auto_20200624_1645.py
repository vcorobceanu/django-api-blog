# Generated by Django 3.0.7 on 2020-06-24 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0004_merge_20200624_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='task',
            name='time_start',
        ),
        migrations.RemoveField(
            model_name='task',
            name='timer_start',
        ),
        migrations.RemoveField(
            model_name='task',
            name='timer_status',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('open', 'Opened'), ('closed', 'Closed')], default='open', max_length=32),
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_begin', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TaskManager.Task')),
            ],
        ),
    ]

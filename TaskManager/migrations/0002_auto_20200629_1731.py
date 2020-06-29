# Generated by Django 3.0.7 on 2020-06-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttask',
            name='status',
            field=models.CharField(choices=[('open', 'Opened'), ('closed', 'Closed')], default='open', max_length=32),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('open', 'Opened'), ('closed', 'Closed')], default='open', max_length=32),
        ),
    ]

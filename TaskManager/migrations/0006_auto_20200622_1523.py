# Generated by Django 3.0.7 on 2020-06-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0005_auto_20200622_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('closed', 'Closed'), ('open', 'Opened')], default='open', max_length=32),
        ),
    ]

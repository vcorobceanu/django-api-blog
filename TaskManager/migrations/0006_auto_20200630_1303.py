# Generated by Django 3.0.7 on 2020-06-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0005_auto_20200630_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.ImageField(upload_to='pictures'),
        ),
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

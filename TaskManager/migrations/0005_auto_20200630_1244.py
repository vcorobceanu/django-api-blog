# Generated by Django 3.0.7 on 2020-06-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0004_auto_20200630_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.FileField(default='no_image.png', upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('in_process', 'In process'), ('finished', 'Finished')], default='in_process', max_length=32),
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='status',
            field=models.CharField(choices=[('closed', 'Closed'), ('open', 'Opened')], default='open', max_length=32),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('closed', 'Closed'), ('open', 'Opened')], default='open', max_length=32),
        ),
    ]

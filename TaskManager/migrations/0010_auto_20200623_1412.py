# Generated by Django 3.0.7 on 2020-06-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0009_auto_20200623_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('open', 'Opened'), ('closed', 'Closed')], default='open', max_length=32),
        ),
    ]

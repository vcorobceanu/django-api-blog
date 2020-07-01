# Generated by Django 3.0.7 on 2020-07-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0012_auto_20200701_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=399)),
                ('file', models.FileField(upload_to='exports')),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('finished', 'Finished'), ('in_process', 'In process')], default='in_process', max_length=32),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-28 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_task_title_alter_task_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Title'),
        ),
    ]

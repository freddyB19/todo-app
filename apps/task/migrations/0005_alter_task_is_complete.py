# Generated by Django 5.0.3 on 2024-03-30 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_alter_task_description_alter_task_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='Status'),
        ),
    ]

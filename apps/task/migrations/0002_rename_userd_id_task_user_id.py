# Generated by Django 5.0.3 on 2024-03-28 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='userd_id',
            new_name='user_id',
        ),
    ]
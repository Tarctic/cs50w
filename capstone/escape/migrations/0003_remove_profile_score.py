# Generated by Django 4.0 on 2022-04-22 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escape', '0002_alter_profile_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='score',
        ),
    ]

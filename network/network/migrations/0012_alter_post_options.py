# Generated by Django 3.2.8 on 2021-12-12 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_post_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-creation',)},
        ),
    ]

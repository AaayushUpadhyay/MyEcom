# Generated by Django 3.1.7 on 2021-05-23 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210522_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='f_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='l_name',
        ),
    ]

# Generated by Django 3.2.3 on 2021-05-29 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210529_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_desc',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]

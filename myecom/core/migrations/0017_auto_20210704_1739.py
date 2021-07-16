# Generated by Django 3.2.4 on 2021-07-04 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_order_created_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'get_latest_by': 'created_on'},
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='default1.jpg', upload_to='profile_pics'),
        ),
    ]

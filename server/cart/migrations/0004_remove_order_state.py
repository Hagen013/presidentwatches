# Generated by Django 2.1.4 on 2019-07-08 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20190708_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
    ]
# Generated by Django 2.1.7 on 2019-03-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20190327_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorypage',
            name='_depth',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
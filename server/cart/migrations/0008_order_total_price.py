# Generated by Django 2.1.4 on 2019-08-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20190817_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

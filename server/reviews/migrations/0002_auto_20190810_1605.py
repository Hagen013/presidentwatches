# Generated by Django 2.1.4 on 2019-08-10 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.PositiveIntegerField(choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1'), (0, '0')], default=10),
        ),
    ]

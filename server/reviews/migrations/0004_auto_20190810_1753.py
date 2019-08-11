# Generated by Django 2.1.4 on 2019-08-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_productreview_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.PositiveIntegerField(choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1'), (0, '0')], default=0),
        ),
    ]

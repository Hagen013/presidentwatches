# Generated by Django 2.1.4 on 2019-11-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20190810_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpage',
            name='has_club_price',
            field=models.BooleanField(default=False),
        ),
    ]
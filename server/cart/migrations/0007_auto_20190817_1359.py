# Generated by Django 2.1.4 on 2019-08-17 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20190816_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='name',
            field=models.CharField(db_index=True, max_length=64, unique=True),
        ),
    ]

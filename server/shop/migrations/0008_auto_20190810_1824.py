# Generated by Django 2.1.4 on 2019-08-10 15:24

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_productpage_rating_overall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpage',
            name='rating_overall',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=shop.models.default_rating),
        ),
    ]

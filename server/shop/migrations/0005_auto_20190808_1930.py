# Generated by Django 2.1.4 on 2019-08-08 16:30

from django.db import migrations
import eav.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_productpage_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='key',
            field=eav.fields.EavSlugField(blank=True, max_length=255, unique=True),
        ),
    ]

# Generated by Django 2.1.4 on 2019-09-17 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20190913_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='resolved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
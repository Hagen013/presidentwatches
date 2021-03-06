# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-21 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_sdek_city_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickpointcitylist',
            name='kladr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kladr.Kladr', unique=True, verbose_name='КЛАДР'),
        ),
        migrations.AlterField(
            model_name='sdekcitylist',
            name='kladr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kladr.Kladr', unique=True, verbose_name='КЛАДР'),
        ),
    ]

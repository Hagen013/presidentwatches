# Generated by Django 2.1.4 on 2019-12-02 16:06

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_order_created_by_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftSalesTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='promocode',
            name='sales',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='datatype',
            field=models.PositiveSmallIntegerField(choices=[(1, 'По брендам'), (2, 'По коллекциям'), (3, 'Приватный'), (4, 'Вручную'), (5, 'Вам подарок')], default=1),
        ),
    ]

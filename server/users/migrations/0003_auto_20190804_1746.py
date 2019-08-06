# Generated by Django 2.1.4 on 2019-08-04 14:46

import core.db.fields.phone
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190718_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=core.db.fields.phone.PhoneNumberField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number'),
        ),
    ]
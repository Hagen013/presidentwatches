# Generated by Django 2.1.4 on 2019-08-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190804_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.PositiveIntegerField(choices=[(1, 'Неизвестно'), (2, 'Мужчина'), (3, 'Женщина')], default=1),
        ),
    ]

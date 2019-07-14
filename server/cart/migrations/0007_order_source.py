# Generated by Django 2.1.4 on 2019-07-08 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_order_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='source',
            field=models.IntegerField(choices=[(1, 'Неизвестно'), (2, 'Корзина'), (3, 'Быстрая покупка'), (4, 'Страница категории')], default=1),
        ),
    ]
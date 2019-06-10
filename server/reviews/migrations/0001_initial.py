# Generated by Django 2.1.4 on 2019-05-29 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0003_categorypage_search_scoring'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='last modification date')),
                ('text', models.TextField(blank=True)),
                ('status', models.PositiveIntegerField(choices=[(10, '10'), (9, '9'), (8, '8'), (7, '7'), (6, '6'), (5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1'), (0, '0')], default=1)),
                ('rating', models.PositiveIntegerField(choices=[(1, 'Новый'), (2, 'Одобрен'), (3, 'Отклонен'), (4, 'Архивирован')], default=10)),
                ('_author', models.CharField(blank=True, max_length=255)),
                ('ip_address', models.GenericIPAddressField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.ProductPage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
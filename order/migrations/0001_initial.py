# Generated by Django 3.2.5 on 2022-03-27 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, editable=False, verbose_name='Model Field create_date')),
                ('update_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Model Field update_date')),
                ('purchase_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Model Order Field purchase_date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Model Product Field user')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Model Receipt Field count')),
                ('create_date', models.DateTimeField(blank=True, verbose_name='Model Field create_date')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Model Field update_date')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='order.order', verbose_name='Model Receipt Field order')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='product.productvariant', verbose_name='Model Receipt Field product_variant')),
            ],
        ),
    ]

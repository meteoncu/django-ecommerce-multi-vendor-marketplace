# Generated by Django 3.2.5 on 2022-03-27 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Model ProductDraft Field title')),
                ('description', models.CharField(max_length=100, verbose_name='Model ProductDraft Field description')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='drafts', to='product.category', verbose_name='Model ProductDraft Field category')),
                ('original', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='drafts', to='product.product', verbose_name='Model ProductDraft Field original')),
            ],
        ),
    ]

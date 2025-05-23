# Generated by Django 5.1.7 on 2025-04-24 10:58

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('sku', models.CharField(help_text='Stock Keeping Unit', max_length=50, unique=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('stock_level', models.PositiveIntegerField(default=0, help_text='Current quantity available in inventory')),
                ('reorder_point', models.PositiveIntegerField(default=10, help_text='Minimum stock level before reordering')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(help_text='Category this product belongs to', on_delete=django.db.models.deletion.PROTECT, related_name='products', to='categories.category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]

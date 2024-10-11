# Generated by Django 5.1.2 on 2024-10-10 15:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0002_alter_transaction_book_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='debt',
            field=models.IntegerField(blank=True, verbose_name=[django.core.validators.MinValueValidator(0)]),
        ),
    ]

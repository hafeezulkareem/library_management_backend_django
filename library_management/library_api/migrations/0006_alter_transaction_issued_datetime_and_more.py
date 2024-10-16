# Generated by Django 5.1.2 on 2024-10-11 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0005_alter_member_email_alter_member_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='issued_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='returned_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

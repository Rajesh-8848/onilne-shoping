# Generated by Django 4.2.9 on 2024-01-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='products',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

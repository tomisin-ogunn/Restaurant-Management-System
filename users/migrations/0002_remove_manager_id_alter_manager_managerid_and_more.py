# Generated by Django 5.1.1 on 2025-01-28 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='id',
        ),
        migrations.AlterField(
            model_name='manager',
            name='managerId',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='waiter',
            name='waiterId',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]

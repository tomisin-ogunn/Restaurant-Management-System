# Generated by Django 5.1.1 on 2025-02-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservationId',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]

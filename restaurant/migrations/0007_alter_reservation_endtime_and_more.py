# Generated by Django 5.1.1 on 2025-02-12 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_alter_reservation_reservation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='endTime',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='startTime',
            field=models.CharField(max_length=50),
        ),
    ]

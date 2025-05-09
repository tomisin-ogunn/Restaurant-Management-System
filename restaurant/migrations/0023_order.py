# Generated by Django 5.1.1 on 2025-03-17 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0022_orderitem_soup_choice_alter_orderitem_desert_sauce_and_more'),
        ('users', '0004_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderId', models.CharField(blank=True, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('total_expected_duration', models.CharField(max_length=50)),
                ('customer_name', models.CharField(max_length=60)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Delayed', 'Delayed'), ('Ready', 'Ready'), ('Delivered', 'Delivered')], default='Pending', max_length=50)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.basket')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.customer')),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.table')),
            ],
        ),
    ]

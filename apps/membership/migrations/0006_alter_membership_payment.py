# Generated by Django 5.0.3 on 2024-05-29 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0005_membership'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='membership', to='payment.payment'),
        ),
    ]

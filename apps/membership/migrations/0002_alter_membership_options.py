# Generated by Django 4.2.4 on 2023-10-16 18:45

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='options',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=50), size=10),
        ),
    ]

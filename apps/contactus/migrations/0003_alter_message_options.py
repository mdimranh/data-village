# Generated by Django 4.2.6 on 2024-03-27 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0002_message_created_at_message_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-id']},
        ),
    ]

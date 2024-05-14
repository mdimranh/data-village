# Generated by Django 4.2.6 on 2024-04-02 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0006_remove_file_folder_remove_file_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="package",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="file",
                to="data.filepackage",
            ),
            preserve_default=False,
        ),
    ]

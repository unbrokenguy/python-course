# Generated by Django 3.2.3 on 2021-05-27 14:33

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_alter_user_confirmation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="confirmation_code",
            field=models.UUIDField(
                default=uuid.UUID("31dc1e51-45f5-4696-a4f6-70b751f01d89"),
                editable=False,
            ),
        ),
    ]

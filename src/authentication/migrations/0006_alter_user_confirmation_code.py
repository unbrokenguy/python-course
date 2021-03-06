# Generated by Django 3.2.3 on 2021-05-28 14:28

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0005_alter_user_confirmation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="confirmation_code",
            field=models.UUIDField(
                default=uuid.UUID("8b66b537-3f33-4988-96bd-1c8177fa2686"),
                editable=False,
            ),
        ),
    ]

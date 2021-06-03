# Generated by Django 3.2.3 on 2021-05-27 15:09

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_alter_user_confirmation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="confirmation_code",
            field=models.UUIDField(
                default=uuid.UUID("34078470-903e-4ce6-ac66-bfa52724a16a"),
                editable=False,
            ),
        ),
    ]

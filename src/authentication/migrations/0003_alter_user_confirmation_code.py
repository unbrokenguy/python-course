# Generated by Django 3.2.3 on 2021-05-26 15:48

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_alter_user_confirmation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="confirmation_code",
            field=models.UUIDField(default=uuid.UUID("0642eef4-2f51-41b0-a469-ce5cc8ea1862"), editable=False),
        ),
    ]

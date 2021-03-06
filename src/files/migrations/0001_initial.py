# Generated by Django 3.2.3 on 2021-05-27 14:33

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import files.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("stats", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to=files.models.file_upload)),
                ("original_name", models.CharField(max_length=255)),
                ("short_url", models.CharField(max_length=255, unique=True)),
                (
                    "expire_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("permanent", models.BooleanField(default=False)),
                ("one_off", models.BooleanField(default=False)),
                ("downloads", models.IntegerField(default=0)),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("views", models.ManyToManyField(to="stats.StatView")),
            ],
        ),
    ]

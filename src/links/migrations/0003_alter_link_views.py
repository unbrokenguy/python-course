# Generated by Django 3.2.3 on 2021-05-26 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0001_initial"),
        ("links", "0002_link_permanent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="views",
            field=models.ManyToManyField(to="stats.StatView"),
        ),
    ]

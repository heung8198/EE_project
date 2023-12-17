# Generated by Django 4.2.7 on 2023-12-16 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PredictionBicycle",
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
                ("station_name", models.CharField(max_length=100)),
                ("rental_date", models.DateField()),
                ("rental_hour", models.IntegerField()),
                ("expected_usage", models.IntegerField()),
                ("temperature", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("rainfall", models.FloatField()),
                ("humidity", models.IntegerField()),
                ("day_of_week", models.JSONField()),
            ],
        ),
    ]
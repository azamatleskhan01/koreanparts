# Generated by Django 5.1.7 on 2025-04-03 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0002_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="image",
            field=models.ImageField(
                blank=True, help_text="Фото товара.", null=True, upload_to="reviews/"
            ),
        ),
    ]

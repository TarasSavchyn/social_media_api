# Generated by Django 4.2.7 on 2023-11-22 20:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(related_name="post_likes", to="social.like"),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-23 22:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("social", "0003_post_comments_alter_post_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="comments",
            field=models.ManyToManyField(
                blank=True, related_name="comment_posts", to="social.comment"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="liked_posts",
                through="social.Like",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
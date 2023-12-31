import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


def social_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.user.email)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "social", filename)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", through="Like")

    comments = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="comment_post",
    )
    image = models.ImageField(upload_to=social_image_file_path, null=True, blank=True)

    def __str__(self):
        return f"Post by {self.user.email} at {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.email} on Post {self.post.id}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on Post {self.post.id}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    bio = models.TextField(blank=True, default="")
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="profile_followers", blank=True
    )
    image = models.ImageField(upload_to=social_image_file_path, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.last_name:
            return self.user.last_name
        else:
            return ""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_likes", through="Like")
    comments = models.ManyToManyField("Comment", blank=True, related_name="post_comments")

    def __str__(self):
        return f"Post by {self.user.email} at {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.email} on Post {self.post.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on Post {self.post.id}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default="")
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="my_followers", blank=True
    )

    def __str__(self):
        return f"Profile of {self.user.email}"

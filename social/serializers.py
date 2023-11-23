from rest_framework import serializers
from .models import Profile, Post, Comment, Like


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "bio",
            "following",
        ]





class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post", "text", "created_at"]
        read_only_fields = ["id", "user", "post", "created_at"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=False)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "likes_count", "comments"]

class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likers = serializers.StringRelatedField(source='likes', many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "likes_count", "comments", "likers"]


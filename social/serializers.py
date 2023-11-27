from rest_framework import serializers
from .models import Profile, Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post", "text", "created_at"]
        read_only_fields = ["id", "user", "post", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "created_at",
            "image",
        ]


class PostListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=False)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "likes_count", "comments", "image"]


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likers = serializers.StringRelatedField(source="likes", many=True, read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "created_at",
            "likes_count",
            "comments",
            "likers",
            "image",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "following", "posts", "image"]

    def get_posts(self, profile):
        posts = Post.objects.filter(user=profile.user)
        serializer = PostListSerializer(posts, many=True)
        return serializer.data


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "bio",
            "following",
            "image"
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "following", "posts", "image"]

    def get_posts(self, profile):
        posts = Post.objects.filter(user=profile.user)
        serializer = PostListSerializer(posts, many=True)
        return serializer.data

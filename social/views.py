from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from social.models import Profile, Post, Like
from social.serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer, PostDetailSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()



    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user_to_follow_profile = self.get_object()
        if not self.request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        current_user_profile = Profile.objects.get(user=self.request.user)
        if current_user_profile.following.filter(pk=user_to_follow_profile.id).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user_to_follow_profile.user == current_user_profile.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_user_profile.following.add(user_to_follow_profile)
        return Response(
            {"detail": "You are now following this user."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user_to_unfollow_profile = self.get_object()

        if not self.request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        current_user_profile = Profile.objects.get(user=self.request.user)

        if user_to_unfollow_profile.user == current_user_profile.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not current_user_profile.following.filter(
            pk=user_to_unfollow_profile.id
        ).exists():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_user_profile.following.remove(user_to_unfollow_profile)

        return Response(
            {"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if Like.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like = Like(user=user, post=post)
        like.save()

        return Response(
            {"detail": "You have liked this post."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def take(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()

        return Response(
            {"detail": "You have unliked this post."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            post.comments.add(serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def delete_comment(self, request, pk=None):
        post = self.get_object()
        user_comments = post.comments.filter(user=request.user)
        user_comments.delete()
        return Response(
            {"detail": "User comments on this post deleted successfully."},
            status=status.HTTP_200_OK,
        )

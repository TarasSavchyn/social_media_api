from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from social.models import Profile, Post, Comment, Like
from social.serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow_profile = self.get_object()
        if not self.request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        current_user_profile = Profile.objects.get(user=self.request.user)
        if current_user_profile.following.filter(pk=user_to_follow_profile.id).exists():
            return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_follow_profile.user == current_user_profile.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        current_user_profile.following.add(user_to_follow_profile)
        return Response({"detail": "You are now following this user."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow_profile = self.get_object()

        if not self.request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        current_user_profile = Profile.objects.get(user=self.request.user)

        if user_to_unfollow_profile.user == current_user_profile.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if not current_user_profile.following.filter(pk=user_to_unfollow_profile.id).exists():
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.following.remove(user_to_unfollow_profile)

        return Response({"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


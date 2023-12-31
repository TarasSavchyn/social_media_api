from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from social.models import Profile, Post, Like
from social.permissions import IsProfileOwnerOrReadOnly
from social.serializers import (
    ProfileSerializer,
    PostListSerializer,
    CommentSerializer,
    PostDetailSerializer,
    PostSerializer,
    ProfileListSerializer,
    ProfileDetailSerializer,
)
from rest_framework import viewsets, status
from social_media.tasks import create_scheduled_post


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        # filtering by email
        email = self.request.query_params.get("email")
        if email:
            queryset = queryset.filter(user__email__icontains=email)
        return queryset

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        user_to_follow_profile = self.get_object()
        current_user_profile = Profile.objects.get(user=self.request.user)
        current_user_profile.following.add(user_to_follow_profile)
        return Response(
            {"detail": "Now you are following this user."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        user_to_unfollow_profile = self.get_object()

        current_user_profile = Profile.objects.get(user=self.request.user)

        current_user_profile.following.remove(user_to_unfollow_profile)

        return Response(
            {"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                type={"type": "string"},
                description="Filter profiles by email.",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [
        IsProfileOwnerOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Post.objects.all()
        # filtering by content
        content = self.request.query_params.get("content")
        if content:
            queryset = queryset.filter(content__icontains=content)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def create_scheduled_post(self, request):
        content = request.data.get("content")
        delay = int(request.query_params.get("delay", 0))

        create_scheduled_post.apply_async(
            kwargs={"user_id": request.user.id, "content": content}, countdown=delay
        )

        return Response(
            {"detail": "Post creation scheduled."}, status=status.HTTP_202_ACCEPTED
        )

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = Like(user=user, post=post)
        like.save()

        return Response(
            {"detail": "You have liked this post."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def take(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = Like.objects.filter(user=user, post=post).first()
        like.delete()

        return Response(
            {"detail": "You have unliked this post."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)
        post.comments.add(serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def delete_comment(self, request, pk=None):
        post = self.get_object()
        user_comments = post.comments.filter(user=request.user)
        user_comments.delete()
        return Response(
            {"detail": "User comments on this post deleted successfully."},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="content",
                type={"type": "string"},
                description="Filter posts by content.",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

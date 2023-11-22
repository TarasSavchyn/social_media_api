from rest_framework.routers import DefaultRouter
from social.views import ProfileViewSet, PostViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"likes", LikeViewSet)

urlpatterns = [] + router.urls

app_name = "social"

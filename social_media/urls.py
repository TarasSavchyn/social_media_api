from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from social_media import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/social/", include("social.urls", namespace="social")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from celery import shared_task
from django.contrib.auth import get_user_model
from social.models import Post

User = get_user_model()

@shared_task
def create_scheduled_post(user_id, content):
    user = User.objects.get(id=user_id)

    # Створення поста
    post = Post.objects.create(user=user, content=content)
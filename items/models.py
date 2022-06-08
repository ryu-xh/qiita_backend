import uuid as uuid
from django.db import models

from users.models import User


class Tag(models.Model):
    """
    タグ
    """

    name = models.CharField(max_length=255, null=False)


class Item(models.Model):
    """
    投稿
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    title = models.CharField(max_length=255, null=False)
    body = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=False)
    tags = models.ManyToManyField(Tag, related_name="posts")

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)


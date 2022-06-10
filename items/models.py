import uuid as uuid

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from users.models import User


class Item(models.Model):
    """
    投稿
    """
    class Meta:
        indexes = [
            GinIndex(fields=['tags'])
        ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    title = models.CharField(max_length=255, null=False)
    body = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items", null=False)
    tags = ArrayField(models.CharField(max_length=255), null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def has_tag(self, tag: str) -> bool:
        """
        この投稿にタグが含まれているか
        """

        return tag in self.tags

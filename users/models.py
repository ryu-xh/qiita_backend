from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    ユーザー
    """

    handle = models.CharField(max_length=32, null=False)
    profile_image_url = models.TextField(blank=False, null=True)

    @property
    def item_count(self) -> int:
        """
        このユーザーの投稿数
        """
        return self.items.count()

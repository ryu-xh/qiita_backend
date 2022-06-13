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

    def is_lgtm(self) -> bool:
        """
        LGTMしているか
        """

        return self.lgtms.exists()

    def has_tag(self, tag: str) -> bool:
        """
        この投稿にタグが含まれているか
        """

        return tag in self.tags

    @property
    def lgtm_count(self) -> int:
        """
        LGTMの数
        """

        return self.lgtms.count()

    def lgtm(self, user: User) -> bool:
        """
        LGTM
        """

        if self.lgtms.filter(user=user).exists():
            return False

        self.lgtms.create(user=user)
        return True

    def unlgtm(self, user: User) -> bool:
        """
        LGTMを解除
        """

        if not self.lgtms.filter(user=user).exists():
            return False

        self.lgtms.filter(user=user).delete()
        return True


class Lgtm(models.Model):
    """
    LGTM
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="lgtms", null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lgtms", null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)


class PopularItem(models.Model):
    """
    人気投稿
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="popular_items", null=False)
    lgtm_count = models.IntegerField(null=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

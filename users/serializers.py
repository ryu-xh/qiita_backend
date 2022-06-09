from rest_framework import serializers

from .models import User


class UserSerializerBase(serializers.ModelSerializer):
    """
    UserのSerializerベースクラス
    """
    class Meta:
        model = User
        fields = (
            'handle',
            'username',
            'profile_image_url',
        )


class UserReadOnlySerializer(UserSerializerBase):
    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields + (
            'item_count',
        )

        read_only_fields = (
            'handle',
            'username',
            'profile_image_url',
            'item_count',
        )


class UserUpsertSerializer(UserSerializerBase):
    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields

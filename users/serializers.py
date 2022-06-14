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

    def create(self, validated_data):
        """
        Userを作成する
        """

        user = User.objects.filter(handle=validated_data['handle'])

        if user.exists():
            raise serializers.ValidationError('handle is already exists')

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Userを更新する
        """

        user = User.objects.filter(handle=validated_data['handle'])

        if user.exists() and instance != user.first():
            raise serializers.ValidationError('handle is already exists')

        instance.handle = validated_data['handle']
        instance.save()

        return instance

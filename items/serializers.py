from rest_framework import serializers

from users.serializers import UserReadOnlySerializer
from .models import Item


class ItemSerializerBase(serializers.ModelSerializer):
    """
    ItemのSerializerベースクラス
    """
    class Meta:
        model = Item
        fields = (
            'uuid',
            'title',
            'body',
            'tags',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
        )


class ItemReadOnlySerializer(ItemSerializerBase):
    class Meta(ItemSerializerBase.Meta):
        fields = ItemSerializerBase.Meta.fields + (
            'user',
        )

        read_only_fields = ItemSerializerBase.Meta.read_only_fields + (
            'title',
            'body',
            'tags',
            'user',
        )

    user = UserReadOnlySerializer()


class ItemUpsertSerializer(ItemSerializerBase):
    """
    ItemのUpsert用Serializer
    """
    class Meta(ItemSerializerBase.Meta):
        fields = ItemSerializerBase.Meta.fields

        read_only_fields = ItemSerializerBase.Meta.read_only_fields

    def create(self, validated_data):
        """
        Itemを作成する
        """

        return Item.objects.create(
            user=self.context['request'].user,
            **validated_data
        )

from rest_framework import viewsets

from qiita_backend.view_base import DisallowModifyOthersMixin
from .filters import ItemFilter
from .models import Item
from .serializers import ItemReadOnlySerializer, ItemUpsertSerializer


class _ItemViewSet(viewsets.ModelViewSet):
    """
    ItemのViewSetベースクラス
    """
    queryset = Item.objects.all()
    filter_class = ItemFilter
    search_fields = ['title', 'body', 'tags', 'user__handle']
    lookup_field = 'uuid'

    def get_object(self):
        return super().get_object()


class ItemViewSet(
    DisallowModifyOthersMixin,
    _ItemViewSet
):
    """
    ItemのViewSet
    """

    def get_serializer_class(self):
        serializer_class = {
            'GET': ItemReadOnlySerializer,
            '__default__': ItemUpsertSerializer
        }

        return serializer_class.get(
            self.request.method,
            serializer_class['__default__']
        )

from rest_framework import viewsets

from .filters import ItemFilter
from .models import Item
from .serializers import ItemReadOnlySerializer, ItemUpsertSerializer


class _ItemViewSet(viewsets.ModelViewSet):
    """
    ItemのViewSetベースクラス
    """
    queryset = Item.objects.all()
    filter_class = ItemFilter
    search_fields = ['title', 'body', 'tags__name', 'user__handle']
    # ordering_fields = ['created_at']
    # ordering = ['-created_at']

    def get_object(self):
        return super().get_object()


class ItemViewSet(_ItemViewSet):
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

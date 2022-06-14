from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.decorators import action

from qiita_backend.view_base import DisallowModifyOthersMixin
from qiita_backend.pagination import CursorPagination
from .filters import ItemFilter
from .models import Item, PopularItem
from .serializers import ItemReadOnlySerializer, ItemUpsertSerializer


class _ItemViewSet(viewsets.ModelViewSet):
    """
    ItemのViewSetベースクラス
    """
    queryset = Item.objects.all()
    filter_class = ItemFilter
    # search_fields = ['title', 'body', 'user__handle']
    lookup_field = 'uuid'
    ordering_fields = ['created_at']
    ordering = ['-created_at']

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

    @action(methods=['POST', 'DELETE'], detail=True, url_path='lgtm')
    def lgtm(self, request, uuid):
        """
        ItemをLGTMしたり解除したり
        """
        item = self.get_object()

        if request.method == 'POST':
            item.lgtm(user=request.user)

        elif request.method == 'DELETE':
            item.unlgtm(user=request.user)

        return self.retrieve(request, uuid)


class TagsViewSet(APIView, CursorPagination):
    """
    タグが含まれるアイテムを取得する
    """

    def get(self, request: Request, tags: str):
        items = Item.objects.filter(tags__contains=[tags])
        queryset = self.paginate_queryset(items, request)
        serializer = ItemReadOnlySerializer(queryset, context={
            'request': request
        }, many=True)
        return self.get_paginated_response(serializer.data)


class PopularItemsViewSet(APIView, CursorPagination):
    """
    人気のアイテムを取得する
    """

    def get(self, request: Request):
        popular_items = PopularItem.objects.all().order_by('-lgtm_count').values_list('item_id', flat=True)
        items = Item.objects.filter(id__in=popular_items)
        queryset = self.paginate_queryset(items, request)
        serializer = ItemReadOnlySerializer(queryset, context={
            'request': request
        }, many=True)
        return self.get_paginated_response(serializer.data)

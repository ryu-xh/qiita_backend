import django_filters as filters

from .models import Item


class ItemFilter(filters.FilterSet):
    class Meta:
        model = Item
        fields = [
            'title',
            'body',
            'user__handle'
        ]

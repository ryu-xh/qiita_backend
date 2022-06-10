from django.urls import include, path
from rest_framework import routers


from .views import (
    ItemViewSet,
    TagsViewSet
)

router = routers.DefaultRouter()
router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
    path('tags/<str:tags>', TagsViewSet.as_view(), name='tags'),
]

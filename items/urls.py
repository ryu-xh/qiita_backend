from django.urls import include, path
from rest_framework import routers


from .views import (
    ItemViewSet
)

router = routers.DefaultRouter()
router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
]

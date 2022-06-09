from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    signin,
    signup,
    UserViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup', signup),
    path('auth/signin', signin),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

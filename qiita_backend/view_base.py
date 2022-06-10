from django.contrib.auth.models import AbstractUser
from rest_framework import viewsets, status
from rest_framework.response import Response


class BaseMixin(viewsets.ModelViewSet):
    def get_current_user(self):
        return self.request.user


class DisallowModifyOthersMixin(BaseMixin):
    def is_update_allowed(self, instance) -> bool:
        user: AbstractUser = self.get_current_user()
        if isinstance(instance, AbstractUser):
            return instance.id == user.id
        elif getattr(instance, 'user', None) is not None:
            return instance.user.id == user.id
        return False

    def update(self, request, *args, **kwargs):
        if not self.is_update_allowed(self.get_object()):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.is_update_allowed(self.get_object()):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)

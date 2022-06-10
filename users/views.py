from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from items.serializers import ItemReadOnlySerializer
from qiita_backend.pagination import CursorPagination
from qiita_backend.view_base import DisallowModifyOthersMixin
from .forms import AuthenticationForm
from .models import User
from .serializers import UserReadOnlySerializer, UserUpsertSerializer


class _UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserReadOnlySerializer
    lookup_field = 'handle'
    ordering = ['-date_joined']

    def get_object(self):
        return super().get_object()


class UserViewSet(
    DisallowModifyOthersMixin,
    _UserViewSet
):

    def get_serializer_class(self):
        serializer_class = {
            'GET': UserReadOnlySerializer,
            '__default__': UserUpsertSerializer
        }

        return serializer_class.get(
            self.request.method,
            serializer_class['__default__']
        )


class SpecificUserItems(APIView, CursorPagination):
    """
    特定ユーザーのアイテムを取得する
    """

    def get(self, request: Request, handle: str):
        user = User.objects.get(handle=handle)
        items = user.items.all()
        queryset = self.paginate_queryset(items, request)
        serializer = ItemReadOnlySerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


@api_view(['POST'])
def signin(request):
    form = AuthenticationForm(request.data)
    if not form.is_valid():
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    data = form.cleaned_data

    user = User.objects.filter(handle=data['handle']).first()

    if user is None or not user.check_password(data['password']):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    refresh_token = RefreshToken.for_user(user)

    return Response({
        'access': str(refresh_token.access_token),
        'refresh': str(refresh_token)
    })


@api_view(['POST'])
def signup(request):
    form = AuthenticationForm(request.data)

    if not form.is_valid():
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    data = form.cleaned_data

    user = User(
        handle=data['handle']
    )

    user.set_password(data['password'])

    try:
        with transaction.atomic():
            user.save()
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)

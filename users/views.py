from django.db import transaction
from psycopg2 import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import AuthenticationForm
from .models import User
from .serializers import UserReadOnlySerializer


class _UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserReadOnlySerializer
    lookup_field = 'handle'
    ordering = ['-date_joined']

    def get_object(self):
        return super().get_object()


class UserViewSet(_UserViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(handle=self.request.user.handle)


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

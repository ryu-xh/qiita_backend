from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.forms import AuthenticationForm
from users.models import User


@api_view(['POST'])
def signin(request):
    form = AuthenticationForm(request.data)
    if not form.is_valid():
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    data = form.cleaned_data

    user = User.objects.get(handle=data['handle'])

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
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)

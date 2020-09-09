from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from ..models import Profile
from django.contrib.auth.models import User
from .serializers import (
    SignUpSerializer
)
from rest_framework.response import Response
from rest_framework import status
from ..models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets


class ObtainTokenPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user=user)
    token['username'] = user.username

    return token


class ObtainTokenPairView(TokenObtainPairView):
  serializer_class = ObtainTokenPairSerializer


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user=user)

  return{
      'refresh': str(refresh),
      'access': str(refresh.access_token)
  }


class ProfileView(viewsets.ModelViewSet):
  permission_classes = [AllowAny]

  def create(self, request):
    data = request.data
    password = data.get('password')
    confirmation_password = data.get('confirm_password')

    serializer = SignUpSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    if not confirmation_password:
      return Response({
          'confirm_password': ['This field is required']
      }, status=status.HTTP_400_BAD_REQUEST)

    if password != confirmation_password:
      return Response({
          'confirm_password': ['Confirm password and password do not match']
      }, status=status.HTTP_400_BAD_REQUEST)

    try:
      User.objects.get(username=data.get('username'))
      return Response({
          'user_name': ['A user with the username exists']
      }, status=status.HTTP_400_BAD_REQUEST)
    except:
      country = data.get('country')
      serializer_data = serializer.data
      serializer_data.pop('country', None)
      user = User.objects.create_user(**serializer_data)

      Profile.objects.create(
          user=user,
          country=data.get('country')
      )

      return Response(
          data=get_tokens_for_user(user=user),
          status=status.HTTP_201_CREATED
      )


from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
  first_name = serializers.CharField(
      max_length=250,
      allow_blank=True,
      required=False
  )
  last_name = serializers.CharField(
      max_length=250,
      allow_blank=True,
      required=False
  )
  email = serializers.EmailField(
      max_length=250,
      allow_blank=True,
      required=False
  )
  username = serializers.CharField(max_length=250)
  password = serializers.CharField(max_length=250)

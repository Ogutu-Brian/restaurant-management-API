from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test import TestCase
from user_profile.models import Profile


class BaseTest(APITestCase):
  client = APIClient()

  def sign_up(self, credentials):
      response = self.client.post(
          path='/profile/sign_up/',
          data=credentials,
          format='json'
      )

      return response

  def clear_all_users(self):
      users = Profile.objects.all()
      [user.delete() for user in users]

  def login(self, credentials):
      response = self.client.post(
          path='/profile/token/',
          data=credentials,
          format='json'
      )

      access_token = response.data.get('access')
      self.client.credentials(
          HTTP_AUTHORIZATION='Bearer {}'.format(access_token)
      )

      return response

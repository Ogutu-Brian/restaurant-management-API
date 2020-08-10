from .base_test import BaseTest
from rest_framework import status


class TestTokenVerification(BaseTest):
  def test_successful_refresh(self):
    self.sign_up({
        'username': 'test@gmail.com',
        'password': 'test password',
        'confirm_password': 'test password'
    })

    response = self.login({
        'username': 'test@gmail.com',
        'password': 'test password',
    })

    response = self.client.post(
        path='/profile/refresh/',
        data=response.data
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual('refresh' in response.data.keys()
                     and 'access' in response.data.keys(), True)

  def test_invalid_token(self):
    response = self.client.post(
        path='/profile/refresh/',
        data={'refresh': 'invalid token'}
    )

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'Token is invalid or expired',
        'code': 'token_not_valid'
    })


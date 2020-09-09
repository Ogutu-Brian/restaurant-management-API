from .base_test import BaseTest
from rest_framework import status


class TestLogIn(BaseTest):
  def setUp(self):
    self.sign_up({
        'username': 'test@gmail.com',
        'password': 'test password',
        'confirm_password': 'test password'
    })

  def test_missing_field(self):
    response = self.login({
        'password': 'test password',
    })

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'username': [
            'This field is required.'
        ]
    })

  def test_unexisting_accout(self):
    response = self.login({
        'username': 'example@gmail.com',
        'password': 'test password',
    })

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'No active account found with the given credentials'
    })

  def test_incorrect_password(self):
    response = self.login({
        'username': 'test@gmail.com',
        'password': 'test pass',
    })

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'No active account found with the given credentials'
    })

  def test_login_success(self):
    response = self.login({
        'username': 'test@gmail.com',
        'password': 'test password',
    })

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual('refresh' in response.data.keys()
                     and 'access' in response.data.keys(), True)

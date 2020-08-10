from .base_test import BaseTest
from rest_framework import status


class TestSignUp(BaseTest):
  def test_missing_field(self):
    response = self.sign_up({
        'password': 'test password',
        'confirm_password': 'test password'
    })

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'username': [
            'This field is required.'
        ]
    })

  def test_mismatching_passwords(self):
    response = self.sign_up({
        'username': 'testuser@gmail.com',
        'password': 'test password',
        'confirm_password': 'another '
    })

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'confirm_password': [
            'Confirm password and password do not match'
        ]
    })

  def test_successful_sign_up(self):
    response = self.sign_up({
        'username': 'test@gmail.com',
        'password': 'test password',
        'confirm_password': 'test password'
    })

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual('refresh' in response.data.keys(), True)
    self.assertEqual('access' in response.data.keys(), True)

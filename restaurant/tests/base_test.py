from user_profile.tests.base_test import BaseTest


class RestaurantBaseTest(BaseTest):
  def setUp(self):
    super().setUp()
    self.sign_up({
        'username': 'test@gmail.com',
        'password': 'test password',
        'confirm_password': 'test password'
    })

    self.login({
        'username': 'test@gmail.com',
        'password': 'test password'
    })

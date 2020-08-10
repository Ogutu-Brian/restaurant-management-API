from .base_test import RestaurantBaseTest
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Restaurant


class TestRestaurant(RestaurantBaseTest):
  def setUp(self):
    return super().setUp()

  def create_restaurant(self):
    return self.client.post(
        path='/restaurant/create/',
        format='json',
        data={
            'name': 'Test restaurant'
        }
    )

  def test_unauthorized_restaurant_creation(self):
    client = APIClient()
    response = client.post(
        path='/restaurant/create/',
        format='json',
        data={
            'name': 'Test restaurant'
        })

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'Authentication credentials were not provided.'
    })

  def test_missing_name(self):
    response = self.client.post(
        path='/restaurant/create/',
        data={},
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'name': [
            'This field is required.'
        ]
    })

  def test_successful_restaurant_creation(self):
    response = self.create_restaurant()
    data = response.data

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual('id' in data and 'name' in data and 'owner' in data, True)

  def test_unauthorized_get_restaurants(self):
    client = APIClient()
    response = client.get(path='/restaurant/')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'Authentication credentials were not provided.'
    })

  def test_successful_fetch_of_restaurants(self):
    response = self.client.get(
        path='/restaurant/'
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, [])

    self.create_restaurant()
    self.create_restaurant()
    self.create_restaurant()

    response = self.client.get(
        path='/restaurant/'
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 3)

  def test_get_unauthorized_single_restaurant(self):
    response = APIClient().get(path='/restaurant/example-id/')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'Authentication credentials were not provided.'
    })

  def test_get_single_restaurant_success(self):
    restaurant = self.create_restaurant().data
    response = self.client.get(
        path='/restaurant/{}/'.format(restaurant.get('id'))
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(restaurant, response.data)

  def test_get_single_restaurant_with_invalid_id(self):
    response = self.client.get(
        path='/restaurant/invalid-id/'
    )

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'error': 'Invalid restaurant id'
    })

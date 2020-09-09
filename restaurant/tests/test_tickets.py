from .base_test import RestaurantBaseTest
from rest_framework.test import APIClient
from rest_framework import status


class TestTickets(RestaurantBaseTest):
  restaurant = {}

  def setUp(self):
    super().setUp()
    self.restaurant = self.client.post(
        path='/restaurant/create/',
        format='json',
        data={
            'name': 'Test restaurant'
        }
    ).data

  def create_ticket(self):
    return self.client.post(
        path='/restaurant/ticket/create/{}/'.format(
            self.restaurant.get('id')
        ),
        data={
            'name': 'My Example ticket',
            'max_purchase_count': 3,
            'amount': 200
        },
        format='json'
    )

  def test_unauthorized_ticket_creation(self):
    response = APIClient().post(path='/restaurant/ticket/create/test/', format='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'Authentication credentials were not provided.'
    })

  def test_invalid_restaurant_id_during_creation(self):
    response = self.client.post(
        path='/restaurant/ticket/create/invalid-id/',
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'error': 'You do not have a restaurant with that id'
    })

  def test_successful_creation_of_ticket(self):
    response = self.client.post(
        path='/restaurant/ticket/create/{}/'.format(self.restaurant.get('id')),
        format='json',
        data={
            'name': 'My Example ticket',
            'max_purchase_count': 3,
            'amount': 200
        }
    )

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    keys = response.data.keys()
    self.assertEqual(['id', 'name', 'max_purchase_count',
                      'number_purchased', 'is_deleted', 'amount', 'restaurant'], list(keys))

  def test_get_tickets_in_restaurant_without_authorization(self):
    response = APIClient().get(path='/restaurant/ticket/test id/', fornat='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'Authentication credentials were not provided.'
    })

  def test_get_tickets_in_restaurant_with_invalid_id(self):
    response = self.client.get(
        path='/restaurant/ticket/incalid-id/', format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'error': 'Invalid restaurant id'
    })

  def test_get_restaurant_tickets_success(self):
    response = self.client.get(
        '/restaurant/ticket/{}/'.format(self.restaurant.get('id')),
        format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, [])

    self.create_ticket()
    self.create_ticket()

    response = self.client.get(
        '/restaurant/ticket/{}/'.format(self.restaurant.get('id')),
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

  def test_unauthorized_ticket_edit(self):
    response = APIClient().put(
        path='/restaurant/ticket/edit/ticket-id/',
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        'detail': 'Authentication credentials were not provided.'
    })

  def test_edit_ticket_with_invalid_id(self):
    response = self.client.put(
        path='/restaurant/ticket/edit/invalid-id/',
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'error': 'invalid ticket id'
    })

  def test_edit_name_successful(self):
    ticket = self.create_ticket().data
    response = self.client.put(
        path='/restaurant/ticket/edit/{}/'.format(ticket.get('id')),
        format='json',
        data={
            'name': 'Edited name'
        }
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data.get('name'), 'Edited name')

  def test_delete_ticket(self):
    ticket = self.create_ticket().data
    response = self.client.put(
        path='/restaurant/ticket/edit/{}/'.format(ticket.get('id')),
        format='json',
        data={
            'is_deleted': True
        }
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data.get('is_deleted'), True)

    response = self.client.get(
        '/restaurant/ticket/{}/'.format(self.restaurant.get('id')),
        format='json'
    )
    self.assertEqual(response.data, [])

  def test_view_single_ticket_with_invalid_id(self):
    response = APIClient().get(
        path='/restaurant/ticket/single/invalid-id/',
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'error': 'Invalid ticket id'
    })

  def test_view_single_ticket_success(self):
    ticket = self.create_ticket()
    response = APIClient().get(
        path='/restaurant/ticket/single/{}/'.format(
            ticket.data.get('id')
        ),
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data.get('id'), ticket.data.get('id'))

  def test_buy_ticket_with_invalid_id(self):
    response = APIClient().put(path='/restaurant/ticket/buy/invalid-id/', format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'error': 'Invalid ticket id'
    })

  def test_successful_buying_of_tickets(self):
    ticket = self.create_ticket()
    response = APIClient().put(
        path='/restaurant/ticket/buy/{}/'.format(ticket.data.get('id')),
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(list(response.data.keys()), ['id', 'ticket'])

  def test_buying_tickets_that_are_sold_out(self):
    def buy_ticket():
      return APIClient().put(
          path='/restaurant/ticket/buy/{}/'.format(ticket.data.get('id')),
          format='json'
      )
    ticket = self.create_ticket()

    buy_ticket()
    buy_ticket()
    response = buy_ticket()
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(list(response.data.keys()), ['id', 'ticket'])

    response = buy_ticket()
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        'error': 'All tickets have been bought'
    })

  def test_get_all_tickets_for_purchase(self):
    response = APIClient().get(
        path='/restaurant/purchase/tickets/',
        format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, [])
    
    self.create_ticket()
    self.create_ticket()
    self.create_ticket()
    
    response = APIClient().get(
        path='/restaurant/purchase/tickets/',
        format='json'
    )
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 3)

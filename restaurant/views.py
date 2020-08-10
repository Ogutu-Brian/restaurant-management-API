from rest_framework.decorators import api_view, permission_classes
from .models import Restaurant, Ticket, Purchase
from .serializers import RestaurantSerializer, TicketSerializer, TicketUpdateSerializer, PurchaseSerializer
from user_profile.models import Profile
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from user_profile.utils.profile_helpers import get_profile_from_api_request
from django.db.models import F
from rest_framework import viewsets


class RestaurantView(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]

  def create(self, request):
    data = request.data
    user = get_profile_from_api_request(request=request)
    data.update({'owner': user.id})
    serializer = RestaurantSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

  def list(self, request):
    user = get_profile_from_api_request(request=request)
    try:
      restaurants = Restaurant.objects.filter(owner__id=user.id)
      serializer = RestaurantSerializer(restaurants, many=True)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except ValidationError:
      return Response({
          'error': 'Invalid restaurant id'
      }, status=status.HTTP_400_BAD_REQUEST)

  def retrieve(self, request, restaurant_id):
    user = get_profile_from_api_request(request=request)

    try:
      restaurant = Restaurant.objects.get(owner__id=user.id, id=restaurant_id)
      serializer = RestaurantSerializer(restaurant, many=False)

      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except (ValidationError, ObjectDoesNotExist):
      return Response({
          'error': 'Invalid restaurant id'
      }, status=status.HTTP_400_BAD_REQUEST)


class TicketView(viewsets.ModelViewSet):
  permission_classes_by_action = {
      'create': [IsAuthenticated],
      'list': [IsAuthenticated],
      'retrieve': [AllowAny],
      'update': [IsAuthenticated]
  }

  def create(self, request, restaurant_id):
    user = get_profile_from_api_request(request=request)

    try:
      restaurant = Restaurant.objects.get(id=restaurant_id, owner__id=user.id)
      data = request.data
      data.update({'restaurant': restaurant.id})
      serializer = TicketSerializer(data=data)
      serializer.is_valid(raise_exception=True)
      serializer.save()

      return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    except (ObjectDoesNotExist, ValidationError):
      return Response({
          'error': 'You do not have a restaurant with that id'
      }, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request, restaurant_id):
    try:
      user = get_profile_from_api_request(request=request)
      tickets = Ticket.objects.filter(
          restaurant__id=restaurant_id,
          is_deleted=False,
          restaurant__owner__id=user.id,
      )
      serializer = TicketSerializer(tickets, many=True)

      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except ValidationError:
      return Response({
          'error': 'Invalid restaurant id'
      }, status=status.HTTP_400_BAD_REQUEST)

  def retrieve(self, request, ticket_id):
    try:
      ticket = Ticket.objects.get(id=ticket_id, is_deleted=False)
      serializer = TicketSerializer(ticket, many=False)

      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except (ValidationError, ObjectDoesNotExist):
      return Response({
          'error': 'Invalid ticket id'
      }, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, ticket_id):
    user = get_profile_from_api_request(request=request)
    try:
      ticket = Ticket.objects.get(id=ticket_id, restaurant__owner__id=user.id)
      ticket_serializer = TicketSerializer(ticket)
      ticket_data = ticket_serializer.data
      ticket_data.pop('restaurant', None)
      ticket_data.pop('id', None)
      ticket_data.update(request.data)

      serializer = TicketUpdateSerializer(data=ticket_data)
      serializer.is_valid(raise_exception=True)
      Ticket.objects.update_or_create(
          id=ticket_id,
          defaults=serializer.data
      )

      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except (ObjectDoesNotExist, ValidationError):
      return Response({
          'error': 'invalid ticket id'
      }, status=status.HTTP_400_BAD_REQUEST)

  def get_permissions(self):
    try:
      return [permission() for permission in self.permission_classes_by_action[self.action]]
    except KeyError:
      return [permission() for permission in self.permission_classes]


class PurchaseTicketsView(viewsets.ModelViewSet):
  permission_classes = [AllowAny]
  queryset = Ticket.objects.filter(is_deleted=False)
  serializer_class = TicketSerializer

  def update(self, request, ticket_id):
    try:
      ticket = Ticket.objects.get(id=ticket_id)

      if ticket.number_purchased >= ticket.max_purchase_count:
        return Response({
            'error': 'All tickets have been bought'
        }, status=status.HTTP_400_BAD_REQUEST)

      ticket.number_purchased = F('number_purchased') + 1
      ticket.save()

      serializer = PurchaseSerializer(data={'ticket': ticket.id})
      serializer.is_valid(raise_exception=True)
      serializer.save()

      return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    except (ObjectDoesNotExist, ValidationError):
      return Response({
          'error': 'Invalid ticket id'
      }, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from .models import Restaurant, Ticket, Purchase


class RestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Restaurant
    fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = '__all__'


class TicketUpdateSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=250, allow_blank=True)
  max_purchase_count = serializers.IntegerField()
  number_purchased = serializers.IntegerField()
  is_deleted = serializers.BooleanField()
  amount=serializers.IntegerField()


class PurchaseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Purchase
    fields = '__all__'

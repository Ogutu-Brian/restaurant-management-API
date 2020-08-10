from django.db import models
from user_profile.models import Profile
import uuid


class Restaurant(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
  name = models.CharField(max_length=250)


class Ticket(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  name = models.CharField(max_length=250)
  max_purchase_count = models.IntegerField()
  number_purchased = models.IntegerField(default=0)
  is_deleted = models.BooleanField(default=False)
  amount = models.IntegerField(default=0)


class Purchase(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  ticket = models.ForeignKey(Ticket, on_delete=models.Case)
  
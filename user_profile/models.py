from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  country = models.CharField(max_length=250, blank=True, null=True)
  
  def __str__(self):
    return self.user.username

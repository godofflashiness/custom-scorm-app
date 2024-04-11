from django.db import models
from django.contrib.auth.models import AbstractUser
from clients.models import Client

class CustomUser(AbstractUser):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=False) 

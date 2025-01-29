from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    google_id = models.CharField(max_length=100, unique=True, null=True)


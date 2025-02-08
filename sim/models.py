from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    google_id = models.CharField(max_length=255, unique=True)
    google_credentials = models.JSONField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)

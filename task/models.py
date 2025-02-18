from django.db import models
from django.conf import settings

class Task(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    q4 = models.TextField()
    q5 = models.TextField()
    day1 = models.BooleanField(default=False)
    day2 = models.BooleanField(default=False)
    day3 = models.BooleanField(default=False)
    day4 = models.BooleanField(default=False)
    day5 = models.BooleanField(default=False)
    day6 = models.BooleanField(default=False)
    day7 = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
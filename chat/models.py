from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    google_event_id = models.CharField(max_length=255)
    summary = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.summary} - {self.start_time}"
    
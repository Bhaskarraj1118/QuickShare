
from django.db import models
import uuid
from django.utils import timezone


class Clipboard(models.Model):
    EXPIRY_CHOICES = [
        (1, "1 Hour"),
        (24, "24 Hours"),
        (168, "7 Days"),
        (0, "Never"),
    ]

    share_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_hours = models.IntegerField(default=24, choices=EXPIRY_CHOICES)

    def is_expired(self):
        if self.expiry_hours == 0:
            return False

        expiry_time = self.created_at + timezone.timedelta(hours=self.expiry_hours)
        return timezone.now() > expiry_time

    def __str__(self):
        return str(self.share_id)

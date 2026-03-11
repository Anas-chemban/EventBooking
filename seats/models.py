from events.models import Event
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from events.models import Venue


class SeatCategory(models.Model):
    name = models.CharField(max_length=50)  # VIP, Regular, Balcony
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
class Seat(models.Model):
    venue = models.ForeignKey(
        'events.Venue',
        on_delete=models.CASCADE,
        related_name='seats'
    )

    category = models.ForeignKey(
        SeatCategory,
        on_delete=models.PROTECT,
        related_name='seats'
    )

    seat_number = models.CharField(max_length=10)  # A1, A2, B5
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('venue', 'seat_number')

    def __str__(self):
        return f"{self.venue.name} - {self.seat_number}"
    
class SeatLock(models.Model):
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='locks'
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='seat_locks'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    locked_until = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['seat', 'event']),
            models.Index(fields=['locked_until']),
        ]

    def __str__(self):
        return f"{self.seat} locked until {self.locked_until}"

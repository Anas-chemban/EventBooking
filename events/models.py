from django.db import models
from django.conf import settings
from django.utils import timezone

class Venue(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()

    def __str__(self):
        return self.name
    
class Event(models.Model):
    EVENT_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    location = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=EVENT_STATUS,
        default='draft'
    )

    # TEMP until seat-based capacity fully replaces it
    booking_limit = models.PositiveIntegerField()

    venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name='events'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['start_time']),
        ]

    def available_slots(self):
        if self.status != 'published':
            return 0

        if self.start_time <= timezone.now():
            return 0

        confirmed = self.bookings.filter(status='confirmed').count()
        return max(self.booking_limit - confirmed, 0)

    def can_book(self):
        return self.available_slots() > 0

    def __str__(self):
        return self.title
    





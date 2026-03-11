from django.utils import timezone
from bookings.models import Booking


def expire_bookings():
    now = timezone.now()
    for booking in Booking.objects.filter(status='pending', expires_at__lt=now):
        booking.mark_expired()

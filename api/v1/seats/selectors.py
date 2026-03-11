# seats/selectors.py
from django.utils import timezone
from seats.models import SeatLock
from tickets.models import Ticket

def available_seats(event):
    now = timezone.now()

    locked_seat_ids = SeatLock.objects.filter(
        event=event,
        locked_until__gt=now
    ).values_list('seat_id', flat=True)

    booked_seat_ids = Ticket.objects.filter(
        booking__event=event
    ).values_list('seat_id', flat=True)

    return event.venue.seats.filter(is_active=True).exclude(
        id__in=locked_seat_ids
    ).exclude(
        id__in=booked_seat_ids
    )

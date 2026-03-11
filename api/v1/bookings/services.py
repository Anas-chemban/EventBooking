from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from bookings.models import Booking
from api.v1.seats.services import lock_seat
from django.conf import settings
from tickets.models import Ticket

LOCK_MINUTES = 10

def create_booking(user, event, seats):
    if not event.can_book():
        raise ValidationError("Event is not available for booking")

    with transaction.atomic():
        booking = Booking.objects.create(
            user=user,
            event=event,
            expires_at=timezone.now() + timedelta(minutes=LOCK_MINUTES)
        )

        for seat in seats:
            lock_seat(seat, event, user)

        return booking
def cancel_booking(booking):
    if booking.status not in ['pending', 'confirmed']:
        return booking

    booking.status = 'cancelled'
    booking.save(update_fields=['status'])
    return booking

def is_refundable(booking):
    refund_deadline = (
        booking.event.start_time
        - timedelta(hours=settings.REFUND_WINDOW_HOURS)
    )
    return timezone.now() < refund_deadline



def cancel_booking_with_refund_check(booking, by_manager=False):
    if booking.status != 'confirmed':
        raise ValueError("Only confirmed bookings can be cancelled")

    refundable = is_refundable(booking)

    if not refundable and not by_manager:
        raise ValueError("Refund window closed")

    # Update booking
    booking.status = 'cancelled'
    booking.save(update_fields=['status'])

    # Expire tickets
    Ticket.objects.filter(
        booking=booking,
        status='active'
    ).update(status='expired')

    return {
        "cancelled": True,
        "refundable": refundable
    }

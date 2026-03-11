from bookings.models import Booking
from tickets.models import Ticket
from django.db import transaction


def cancel_event_and_refund(event):
    """
    Cancels an event and invalidates all related bookings & tickets.
    Refund is handled externally (payment layer).
    """

    with transaction.atomic():
        # 1. Cancel event
        event.status = 'cancelled'
        event.save(update_fields=['status'])

        # 2. Cancel all confirmed bookings
        bookings = Booking.objects.filter(
            event=event,
            status='confirmed'
        )

        bookings.update(status='cancelled')

        # 3. Expire all active tickets
        Ticket.objects.filter(
            booking__event=event,
            status='active'
        ).update(status='expired')

    return True

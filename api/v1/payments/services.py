import razorpay
from django.conf import settings
from seats.models import SeatLock
from bookings.models import Booking

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET)
)


def create_payment_order(booking: Booking):

    if booking.status != "pending":
        raise ValueError("Booking is not pending")

    if booking.is_expired():
        raise ValueError("Booking expired")

    locks = SeatLock.objects.filter(
        event=booking.event,
        user=booking.user
    )

    if not locks.exists():
        raise ValueError("No seats locked for booking")

    amount = sum(
        lock.seat.category.price for lock in locks
    )

    order = client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "receipt": f"booking_{booking.id}",
        "notes": {
            "booking_id": booking.id
        },
        "payment_capture": 1
    })

    booking.payment_status = "pending"
    booking.payment_reference = order["id"]
    booking.save(update_fields=["payment_status", "payment_reference"])

    return order
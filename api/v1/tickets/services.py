import qrcode
from io import BytesIO
from datetime import timedelta

from django.core.files import File
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from django.db import transaction

from tickets.models import Ticket
from seats.models import SeatLock

def generate_ticket_qr(ticket):
    data = (
        f"TICKET:{ticket.id}|"
        f"EVENT:{ticket.booking.event.id}|"
        f"SEAT:{ticket.seat.seat_number}"
    )

    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    ticket.qr_code.save(
        f"ticket_{ticket.id}.png",
        File(buffer),
        save=True
    )
def confirm_booking_and_issue_tickets(booking):
    if booking.status != "pending":
        raise ValueError("Only pending bookings can be confirmed")

    now = timezone.now()

    with transaction.atomic():
        locks = SeatLock.objects.select_for_update().filter(
            event=booking.event,
            user=booking.user,
            locked_until__gt=now
        )

        if not locks.exists():
            raise ValueError("No active seat locks found")

        tickets = []

        for lock in locks:
            ticket = Ticket.objects.create(
                booking=booking,
                seat=lock.seat
            )
            generate_ticket_qr(ticket)
            tickets.append(ticket)

        locks.delete()

        booking.status = "confirmed"
        booking.save(update_fields=["status"])

    # 🔥 email AFTER DB commit
    send_ticket_email(booking)

    return tickets
def send_ticket_email(booking):
    email = EmailMessage(
        subject=f"Your tickets for {booking.event.title}",
        body=(
            f"Your booking is confirmed.\n\n"
            f"Event: {booking.event.title}\n"
            f"Date: {booking.event.start_time}\n"
            f"Venue: {booking.event.venue.name}"
        ),
        to=[booking.user.email],
    )

    for ticket in booking.tickets.all():
        if ticket.qr_code:
            email.attach_file(ticket.qr_code.path)

    email.send()
def check_in_ticket(ticket):
    if ticket.status != "active":
        raise ValueError("Ticket already used or invalid")

    ticket.status = "used"
    ticket.save(update_fields=["status"])
def cancel_tickets_partial(booking, ticket_ids, by_manager=False):
    tickets = Ticket.objects.filter(
        id__in=ticket_ids,
        booking=booking,
        status="active"
    )

    if not tickets.exists():
        raise ValueError("No valid tickets to cancel")

    refundable = True

    if not by_manager:
        refund_deadline = (
            booking.event.start_time
            - timedelta(hours=settings.REFUND_WINDOW_HOURS)
        )

        if timezone.now() >= refund_deadline:
            raise ValueError("Refund window closed")

    tickets.update(status="expired")

    remaining = booking.tickets.filter(status="active").count()
    if remaining == 0:
        booking.status = "cancelled"
        booking.save(update_fields=["status"])

    return {
        "cancelled_tickets": tickets.count(),
        "booking_cancelled": remaining == 0,
        "refundable": refundable
    }

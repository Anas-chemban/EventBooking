import json
from django.http import HttpResponse
from django.conf import settings
from bookings.models import Booking
from api.v1.tickets.services import confirm_booking_and_issue_tickets
from api.v1.payments.services import client


def razorpay_webhook(request):

    payload = request.body
    signature = request.headers.get("X-Razorpay-Signature")

    try:
        client.utility.verify_webhook_signature(
            payload,
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )
    except:
        return HttpResponse(status=400)

    event = json.loads(payload)

    if event["event"] == "payment.captured":

        payment = event["payload"]["payment"]["entity"]

        booking_id = payment["notes"]["booking_id"]

        booking = Booking.objects.get(id=booking_id)

        if booking.payment_status != "paid":

            booking.payment_status = "paid"
            booking.save(update_fields=["payment_status"])

            confirm_booking_and_issue_tickets(booking)

    return HttpResponse(status=200)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from events.models import Event
from .models import Booking
from .utils import send_ticket_email


class BookEventAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        # ❌ Booking closed
        if not event.is_booking_open:
            return Response({"error": "Bookings closed"}, status=400)

        # ❌ Event full
        if event.bookings.count() >= event.booking_limit:
            return Response({"error": "Event full"}, status=400)

        # ✅ CREATE BOOKING (DB commit point)
        booking = Booking.objects.create(
            user=request.user,
            event=event
        )

        # 🎟️ SEND QR + EMAIL (AFTER SAVE)
        send_ticket_email(booking)

        return Response({
            "message": "Booking successful. Ticket sent to your email."
        })

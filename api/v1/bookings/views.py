from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.v1.accounts.permissions import IsManager
from events.models import Event
from api.v1.bookings.services import cancel_booking_with_refund_check, create_booking, cancel_booking
from api.v1.bookings.serializers import BookingSerializer
from bookings.models import Booking
from seats.models import Seat


class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_id = request.data.get('event_id')
        seat_ids = request.data.get('seats', [])

        event = Event.objects.get(id=event_id)
        seats = Seat.objects.filter(id__in=seat_ids)

        booking = create_booking(
            user=request.user,
            event=event,
            seats=seats
        )

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id, user=request.user)
        cancel_booking(booking)
        return Response({"message": "Booking cancelled"})
class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        booking = Booking.objects.get(
            id=booking_id,
            user=request.user
        )

        result = cancel_booking_with_refund_check(booking)

        return Response({
            "message": "Booking cancelled",
            "refundable": result["refundable"]
        })


class ForceCancelBookingView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)

        cancel_booking_with_refund_check(
            booking,
            by_manager=True
        )

        return Response({
            "message": "Booking cancelled by manager"
        })
